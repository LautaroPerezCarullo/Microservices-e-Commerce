from .base_ms_managment import base_MS
class MS_CatalogService(base_MS):

    def __init__(self):
        super().__init__("CATALOG_SERVICE_URL")

    def get_catalog(self):
        response = self._ms_request("GET", "/products", "Catalog", "getting")
        if response:
            return response.json()
    def get_product(self, product_id):
        response = self._ms_request("GET", f"/products/{product_id}", "Product", "getting")
        if response:
            return response.json()