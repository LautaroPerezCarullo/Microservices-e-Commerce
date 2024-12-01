class Response_Management():
    def __init__(self, e):
        error_str = str(e)
        
        # Extraer mensaje y código de estado
        start_msg = error_str.find("ServiceException('") + len("ServiceException('")
        end_msg = error_str.find(" (Status Code:")
        self.message = error_str[start_msg:end_msg]
        
        start_code = error_str.find("(Status Code:") + len("(Status Code:")
        end_code = error_str.find(")", start_code)
        self.status_code = int(error_str[start_code:end_code])

    def to_response(self):
        return {"message": self.message}, self.status_code