import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
from dotenv import load_dotenv
from pathlib import Path


basedir = os.path.abspath(Path(__file__).parents[3])
load_dotenv(os.path.join(basedir, '.env'))


class MS_CatalogService:

    def __init__(self):
        self.catalog_url = os.getenv("CATALOG_SERVICE_URL")

    def get_catalog(self):
        response = requests.get(f"{self.catalog_url}/products", verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting catalog")
    
    def get_product(self, product_id):
        response = requests.get(f"{self.catalog_url}/products/{product_id}", verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error getting product")