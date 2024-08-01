from typing import Type

from ._base import AbstractFlow
from ._exceptions import (
    EmptyFlowError,
    InvalidFormatError,
    NotSupportedFlowError,
)

# TODO: build this register dynamically in python
# with either inspect module or dir(_flow)...
register: dict[str, Type] = {}


def flow_matcher(content: str, file_name: str) -> AbstractFlow:
    """Utility to match the Flow import class based on what specified
    in the file.add()

    Raises error if the flow name is not found or the file is invalid"""

    if not content:
        raise EmptyFlowError("The file is empty")

    # TODO: move this out, it's a temporary fix for a circular import
    from ._flow import D0010002  # noqa

    register["D0010002"] = D0010002

    lines = content.split("\n")
    try:
        values = lines[0].split("|")

        # TODO: rename something with his proper name...
        _, something, flow_name_version, _, _, _, _, datetime, *_ = values

        if flow_name_version not in register:
            raise NotSupportedFlowError(flow_name_version)

        class_ = register[flow_name_version]
        obj = class_(content=content, file_name=file_name)
        return obj

    except IndexError as e:
        raise InvalidFormatError(
            f"The file '{file_name}' is in an invalid format"
        ) from e
