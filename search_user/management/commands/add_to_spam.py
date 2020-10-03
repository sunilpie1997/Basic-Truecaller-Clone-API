from django.core.management.base import BaseCommand, CommandError
from search_user.models import PhoneDirectory



class Command(BaseCommand):
    help = "adds multiple phone no's to spam.If phone no exists,increase spam score"

    def add_arguments(self, parser):
        parser.add_argument('contacts', nargs='+', type=str)

    def handle(self, *args, **options):
        try:

            for phone in options['contacts']:
                obj,is_created=PhoneDirectory.objects.get_or_create(phone=phone)
                
                if not is_created:
                    obj.updateSpamScore()
                    obj.save()

            self.stdout.write(self.style.SUCCESS('Successfully added phone numbers to spam'))
        except Exception as error:
            print(error)