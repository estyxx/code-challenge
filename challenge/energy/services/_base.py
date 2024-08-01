from django.db import transaction

from challenge.energy.models import FlowImportFiles

from ._exceptions import FileAlreadyImportedError


class AbstractFlow:
    """Abstract class for Flow imports classes"""

    def __init__(self, content: str, file_name: str) -> None:
        self.content = content
        self.file_name = file_name

    def log_import(self):
        """Wrapper around the flow execution to save the Flow file
        in the database.

        If there is an error in the import it will r"""

        import_log, created = FlowImportFiles.objects.get_or_create(
            content=self.content,
            name=self.file_name,
        )
        print(import_log, import_log.successful)

        if import_log.successful:
            raise FileAlreadyImportedError(self.file_name)

        return import_log

    @transaction.atomic
    def execute(self):
        raise NotImplementedError()
