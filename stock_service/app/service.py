from .model import Stock
from .repository import StockRepository
from app import db, cache
import redis
from config.cache_config import cache_config
from .exceptions import InsufficientStockError
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from sqlalchemy.exc import OperationalError
import logging
logging.basicConfig(level=logging.INFO)

repository = StockRepository()
redis_client = redis.StrictRedis(
    host=cache_config.get('CACHE_REDIS_HOST'),
    port=cache_config.get('CACHE_REDIS_PORT'),
    db=cache_config.get('CACHE_REDIS_DB'),
    password=cache_config.get('CACHE_REDIS_PASSWORD'),
)

class StockService:

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def save_output(self, stock: Stock) -> Stock:
        cache_key = f"current_stock_product:{stock.product_id}"
        lock_key = f"lock:{cache_key}"

        # Crear un lock para la clave específica
        lock = redis_client.lock(lock_key, timeout=10)

        if lock.acquire(blocking = True):
            #Save new stock
            self.existing_stock = cache.get(cache_key)
            if not self.existing_stock:
                self.existing_stock = self.calculate_stock(stock.product_id)
                cache.set(cache_key, self.existing_stock, timeout = 10)
            logging.info(f"Exisiting Stock: {self.existing_stock}. Set Cache")

            try:
                if stock.amount > self.existing_stock:
                    raise InsufficientStockError(f"Insufficient Stock, Product {stock.product_id}")
                else:
                    new_existing_stock = self.existing_stock - stock.amount
                    logging.info(f"Exisiting Stock: {new_existing_stock}. Set Cache")
                    cache.set(cache_key, new_existing_stock, timeout = 10)
                    return repository.save(stock)
                
            except OperationalError as e:
                logging.error(f"Error connecting database: {str(e)}")
                db.session.rollback()
                raise 

            finally:
                lock.release()  # Liberar el lock
        else:
            raise Exception("Unable to acquire lock for stock update.")

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def save_input(self, stock: Stock) -> Stock:
        cache_key = f"current_stock_product:{stock.product_id}"
        lock_key = f"lock:{cache_key}"

        lock = redis_client.lock(lock_key, timeout=10)

        if lock.acquire(blocking=True):
            
            self.existing_stock = cache.get(cache_key)
            if not self.existing_stock:
                self.existing_stock = self.calculate_stock(stock.product_id)
                cache.set(cache_key, self.existing_stock, timeout=10)

            try:
                new_existing_stock = self.existing_stock + stock.amount
                logging.info(f"Exisiting Stock: {new_existing_stock}. Set Cache")
                cache.set(cache_key, new_existing_stock, timeout = 10)
                return repository.save(stock)

            except OperationalError as e:
                logging.error(f"Error connecting database: {str(e)}")
                db.session.rollback()
                raise

            finally:
                lock.release()
        else:
            raise Exception("Unable to acquire lock for stock update.")

    @retry(wait=wait_fixed(3), stop=stop_after_attempt(5), retry=retry_if_exception_type(OperationalError))
    def calculate_stock(self, product_id: int) -> int:
        try:
            return repository.calculate_stock(product_id)
        
        except OperationalError as e:
            logging.error(f"Error connecting database: {str(e)}")
            db.session.rollback()
            raise 