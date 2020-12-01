from django.contrib.auth import get_user_model
from django.core.management.commands.test import Command as BaseCommand

from core.models import Url


class Command(BaseCommand):
    help = 'Populate the database with a sample user and URL'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        User.objects.count()

        user_data = {
            'username': 'tiago',
            'password': '12345678',
            'email': 'tiagoprn@gmail.com',
        }
        new_user = User(**user_data)
        new_user.save()

        User.objects.all()
        tiago = User.objects.first()

        Url.objects.count()
        tiago_url = Url(
            name='bla', original_url='https://www.osnews.com', user=tiago
        )
        tiago_url.save()

        must_have_values = ['shortened_hash', 'sanitized_url']

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
