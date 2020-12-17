from django.contrib.auth import get_user_model
from django.core.management.commands.test import Command as BaseCommand

from core.models import Link


class Command(BaseCommand):
    help = 'Populate Links from a csv'

    # TODO: this method is here just to be used as a reference.
    #       Delete after finishing the actual handler below.
    def sample_creation_handle(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
        User = get_user_model()
        User.objects.count()

        user_data = {
            'username': 'tiago',
            'password': '12345678',
            'email': 'tiago@example.com',
        }
        new_user = User(**user_data)
        new_user.save()

        User.objects.all()
        tiago = User.objects.first()

        Link.objects.count()
        tiago_url = Link(
            name='autotest', original_link='https://www.osnews.com', user=tiago
        )
        tiago_url.save()

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='Specifies the username that will own imported links.',
        )
        parser.add_argument(
            '--csv-file-path',
            dest='csv_file_path',
            default=None,
            help=(
                'Specifies the csv file path that contains '
                'the links to be imported.'
            ),
        )

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        Call the command with:

        python personal_api/manage.py import_links_from_csv \
            --username=tiago --csv-file-path=/tmp/links.csv

        """
        username = options.get('username')
        csv_file_path = options.get('csv_file_path')

        # TODO: validate if the user with the username exists
        # TODO: validate if the csv_file_path exists

        self.stdout.write(
            f'Importing csv file "{csv_file_path}" '
            f'for username "{username}"... '
        )

        # TODO: continue importing from here using pandas
