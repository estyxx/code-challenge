class UploadError(Exception):
    """Error occour when processing the CSV file"""

    def __init__(self, message: str) -> None:
        self.message = message


class EmptyFileError(UploadError):
    """Raised when the file has no values rows"""

    pass


class FileNotValidError(UploadError):
    pass


class ConsumptionAlreadyProcessedError(UploadError):
    """Raised when the Consumption of the user it's already in the database"""
