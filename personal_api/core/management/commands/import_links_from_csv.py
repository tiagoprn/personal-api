import os
import sys

from django.contrib.auth import get_user_model
from django.core.management.commands.test import Command as BaseCommand

from core.models import Link

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate Links from a csv'

    # TODO: this method is here just to be used as a reference.
    #       Delete after finishing the actual handler below.
    def sample_creation_handle(
        self, *args, **kwargs
    ):  # pylint: disable=unused-argument
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
            required=True,
            default=None,
            help='The username that will own imported links.',
        )
        parser.add_argument(
            '--csv-file-path',
            dest='csv_file_path',
            required=True,
            default=None,
            help=(
                'The full csv file path that contains links to be imported.'
            ),
        )

    def validate_user(self, username: str) -> User:
        links_user = User.objects.filter(username=username).first()
        if not links_user:
            available_users = User.objects.values_list(
                'username', flat=True
            ).order_by('username')
            message = f'There is no use with username={username}. '
            if len(available_users) > 0:
                message += f'Available users: {", ".join(available_users)}'
            else:
                message += (
                    'There are no available users, '
                    'at least one must be created manually.'
                )
            self.stdout.write(self.style.ERROR(message))
            sys.exit(1)
        return links_user

    def finish_if_csv_file_does_not_exist(self, path: str) -> bool:
        if not os.path.exists(path):
            message = f'There is not a file at filesystem path "{path}".'
            self.stdout.write(self.style.ERROR(message))
            sys.exit(1)

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        To test manually:

        create-admin-superuser-without-input username=admin1 \
            password=12345678 email=admin1@gmail.com;

        python personal_api/manage.py import_links_from_csv \
            --username=admin1 --csv-file-path=/tmp/links.csv

        """
        username = options.get('username')
        csv_file_path = options.get('csv_file_path')

        links_user = self.validate_user(username)
        self.finish_if_csv_file_does_not_exist(csv_file_path)

        self.stdout.write(
            f'Importing csv file "{csv_file_path}" '
            f'for username "{links_user.username}"... '
        )

        # TODO: continue importing from here using pandas
