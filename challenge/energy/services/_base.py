from typing import Type

from django.db import transaction

from ._exceptions import EmptyFlowError, InvalidFormatError, NotSupportedFlowError
from ._flow import D0010002


class AbstractFlow:
    """Abstract class for Flow imports classes"""

    def __init__(self, content: str, file_name: str) -> None:
        self.content = content
        self.file_name = file_name

    @transaction.atomic
    def execute(self):
        raise NotImplementedError()


# TODO: build this register dinamically in python
register: dict[str, Type] = {"D0010002": D0010002}


def flow_matcher(content: str, file_name: str) -> AbstractFlow:
    """Utility to match the Flow import class based on what specified
    in the file.add()

    Raises error if the flow name is not found or the file is invalid"""

    if not content:
        raise EmptyFlowError("The file is empty")

    lines = content.split("\n")
    try:
        flow_name_version = lines[0].split("|")[3]

        if flow_name_version not in register:
            raise NotSupportedFlowError(flow_name_version)

        class_ = register[flow_name_version]
        obj = class_(content=content, file_name=file_name)
        return obj

    except IndexError as e:
        raise InvalidFormatError(
            f"The file '{file_name}' is in an invalid format"
        ) from e
