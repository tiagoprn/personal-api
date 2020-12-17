from django.contrib.auth import get_user_model
from django.core.management.commands.test import Command as BaseCommand

from core.models import Link


class Command(BaseCommand):
    help = 'Populate the database with a sample user and URL'

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
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

        must_have_values = ['shortened_hash', 'sanitized_link']

        success = True

        for value in must_have_values:
            if not getattr(tiago_url, value):
                self.stderr.write(
                    f'Missing value for {value}. '
                    f'The django signal was probably not called.'
                )
                success = False

        if success:
            self.stdout.write(f'SUCCESS! Object properties={vars(tiago_url)}')

        # Cascadingly deletes the created user and all its Links,
        # including the one created here.
        User.objects.get(id=tiago.id).delete()
