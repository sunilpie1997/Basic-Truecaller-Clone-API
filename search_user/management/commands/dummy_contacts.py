from django.core.management.base import BaseCommand, CommandError
from search_user.models import PhoneDirectory



class Command(BaseCommand):
    help = 'adds multiple dummy phone_numbers to phone directory at once'

    def add_arguments(self, parser):
        parser.add_argument('contacts', nargs='+', type=str)

    def handle(self, *args, **options):
        try:

            for phone in options['contacts']:
                PhoneDirectory.objects.get_or_create(phone=phone)

            self.stdout.write(self.style.SUCCESS('Successfully added phone numbers'))
        except Exception as error:
            print(error)