class FlowException(Exception):
    pass


class EmptyFlowError(FlowException):
    pass


class InvalidFormatError(FlowException):
    pass


class NotSupportedFlowError(FlowException):
    def __init__(self, name: str):
        self.message = f"Flow '{name}' not supported"
        super().__init__(self.message)


class FileAlreadyImportedError(FlowException):
    def __init__(self, filename: str):
        self.message = (
            f"The flow file '{filename}' has already been imported. Aborting."
        )

        super().__init__(self.message)
