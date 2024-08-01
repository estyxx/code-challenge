from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from challenge.energy import services


class Command(BaseCommand):
    help = "Imports flow files. (Supported only D0010)"

    def add_arguments(self, parser) -> None:
        parser.add_argument("file", type=str)

    def handle(self, *args, **options) -> None:
        file = Path(options["file"])

        if not file.exists():
            raise CommandError('File "%s" not found' % file)

        content = file.read_text()
        if not content:
            raise CommandError("File is empty!")

        try:
            flow_command = services.flow_matcher(content=content, file_name=file.name)
            flow_command.execute()
        except services.FlowException as e:
            raise CommandError(f"Something went wrong while executing: {e}") from e

        self.stdout.write(self.style.SUCCESS("Successfully imported"))
