class ServiceException(Exception):
    def __init__(self, message, status_code):
        super().__init__(f"{message} (Status Code: {status_code})")
        self.message = message
        self.status_code = status_code

class RetryableRequestException(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception
        super().__init__(f"Retryable error: {str(original_exception)}")


