import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
from dotenv import load_dotenv
from pathlib import Path
import urllib3
from .exceptions import ServiceException, RetryableRequestException
import logging
logging.basicConfig(level=logging.INFO)

basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))
urllib3.disable_warnings()

class base_MS:
    
    def __init__(self, url):
        self.ms_url = os.getenv(url)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(RetryableRequestException))
    def _ms_request(self, method, endpoint, ms, type, json_data=None):
        url = f"{self.ms_url}/{endpoint}"
        try:
            response = requests.request(method, url, json = json_data, verify=False)

            try:
                json_response = response.json()  # Intenta parsear la respuesta como JSON
            except requests.exceptions.JSONDecodeError:
                json_response = {"error": "Invalid JSON response", "content": response.text}
            
            response.raise_for_status()
            
            if type == "posting":
                self.id = response.json().get("data", {}).get("id")
                logging.info(f"Successful {ms}: {method} {url} | Payload: {json_data} | "f"Response: {response.status_code} - {response.text}")
            elif type == "compesating":
                logging.info(f"Successful {ms} compensation: {method} {url} | Payload: {json_data} | "f"Response: {response.status_code} - {response.text}")
            elif type == "getting":
                logging.info(f"Successful {ms} obtaining : {method} {url}")
                return response
        
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logging.warning(f"Retrying request due to: {e}")
            raise RetryableRequestException(e)
        
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            message = json_response.get("message", "Unknown error")
            
            if status_code in {502, 503, 504, 429}:
                logging.warning(f"Retrying request due to: {e}")
                raise RetryableRequestException(e)
            else:
                raise ServiceException(message, status_code)

        except requests.exceptions.RequestException as e:
            logging.error(f"Unexpected request error: {e}")
            error_message = "Unknown request error"
            status_code = 500
            if response is not None:
                try:
                    error_message = json_response.get('message', response.text)
                    status_code = response.status_code
                except Exception:
                    error_message = "Invalid response format"
            raise ServiceException(error_message, status_code if response else 500)

        except Exception as e:
            logging.info(response.json().get('message'))
            error_message = "Unexpected error"
            status_code = 500
            if response is not None:
                try:
                    error_message = json_response.get('message', "Unknown error")
                    status_code = response.status_code
                except Exception:
                    error_message = "Invalid response format"

            logging.error(error_message)
            raise ServiceException(error_message, status_code)