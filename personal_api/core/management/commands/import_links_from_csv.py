import logging
import os
import sys
from functools import partial
import pandas

from django.contrib.auth import get_user_model
from django.core.management.commands.test import Command as BaseCommand

from core.models import Link

User = get_user_model()

logger = logging.getLogger(__name__)


def import_link(user: User, link: str):
    try:
        new_url = Link(original_link=link, user=user)
        new_url.save()
        message = f'Successfully saved link="{link}" (id="{new_url.id}")'
        logger.info(message)
    except Exception as ex:
        message = f'Exception trying to save link="{link}": {ex}'
        logger.error(message)


def print_value(link: str):
    print(link)


class Command(BaseCommand):
    help = 'Populate Links from a csv'

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

    def validate_existing_columns(self, dataframe):
        mandatory = {'link'}
        existing_columns = mandatory.intersection(set(dataframe.columns))
        if not existing_columns:
            message = f'Mandatory columns missing from file: {mandatory}'
            self.stdout.write(self.style.ERROR(message))
            sys.exit(1)

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        """
        To test manually:
        make local-links-csv-import-test
        """

        username = options.get('username')
        csv_file_path = options.get('csv_file_path')

        links_user = self.validate_user(username)
        self.finish_if_csv_file_does_not_exist(csv_file_path)

        self.stdout.write(
            f'Importing csv file "{csv_file_path}" '
            f'for username "{links_user.username}"... '
        )

        dataframe = pandas.read_csv(csv_file_path)
        self.validate_existing_columns(dataframe)

        dataframe.link.apply(lambda x: import_link(link=x, user=links_user))
