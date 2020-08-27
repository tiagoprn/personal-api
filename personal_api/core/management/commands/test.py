from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    help = (
        "Wrap Django's built-in test command "
        "to always delete the database if it exists"
    )

    def handle(self, *test_labels, **options):
        options["interactive"] = False
        return super().handle(*test_labels, **options)
