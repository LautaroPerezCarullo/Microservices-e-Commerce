from .base_ms_managment import base_MS
class MS_PaymentService(base_MS):
    
    def __init__(self):
        super().__init__("PAYMENT_SERVICE_URL")

    def payment_processing(self, product_id, price, payment_method):
        return self._ms_request("POST", "/payments/add", "Payment", "posting", json_data={"product_id": product_id, "price": price, "payment_method": payment_method})
    
    def cancel_payment(self, payment_id):
        return self._ms_request("POST", f"/payments/{payment_id}", "Payment", "deleting")