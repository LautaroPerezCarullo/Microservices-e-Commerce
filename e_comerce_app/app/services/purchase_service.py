from .base_ms_managment import base_MS
class MS_PurchaseService(base_MS):
    
    def __init__(self):
        super().__init__("PURCHASE_SERVICE_URL")

    def purchase_processing(self, product_id, delivery_address):
        return self._ms_request("POST", "purchases/add", "Purchase", "posting", json_data={"product_id": product_id, "delivery_address": delivery_address})
    
    def cancel_purchase(self, purchase_id):
        return self._ms_request("DELETE", f"purchases/{purchase_id}", "Purchase", "deleting")
        