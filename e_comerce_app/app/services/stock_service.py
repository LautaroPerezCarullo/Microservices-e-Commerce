from .base_ms_managment import base_MS
class MS_StockService(base_MS):
    
    def __init__(self):
        super().__init__("STOCK_SERVICE_URL")
        self.id = None

    def stock_transaction(self, product_id, amount, input_output):
        return self._ms_request("POST", "stocks/output", "Stock Transaction", "posting", json_data = {"product_id": product_id, "amount": amount, "input_output": input_output})

    def stock_compensation(self, product_id, amount, input_output):
        return self._ms_request("POST", "stocks/intput", "Stock", "posting", json_data = {"product_id": product_id, "amount": amount, "input_output": input_output})