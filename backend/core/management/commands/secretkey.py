from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Generate a Django SECRET_KEY"

    def add_arguments(self, parser):
        parser.add_argument(
            "--env",
            action="store_true",
            help="Output in ENV format: DJANGO_SECRET_KEY=...",
        )
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        key = get_random_secret_key()

        if options["env"]:
            return self.stdout.write(f"DJANGO_SECRET_KEY={key}")
        return self.stdout.write(key)
