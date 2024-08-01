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
