from django.core.management.base import BaseCommand, CommandError
from accounts.models import User


"""
all the arguements listed below need to be provided to create dummy user

"""
class Command(BaseCommand):
    help = 'adds dummy users (registered) for rest api'

    def add_arguments(self, parser):
        parser.add_argument('username',type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('password',type=str)
        parser.add_argument('email',type=str)


    def handle(self, *args, **options):
        username=options["username"]
        password=options["password"]
        email=options["email"]
        name=options["name"]

        try:
            User.objects.create_user(username=username,password=password,email=email,first_name=name)
            self.stdout.write(self.style.SUCCESS('Successfully created user'))
        except Exception as error:
            print(error)