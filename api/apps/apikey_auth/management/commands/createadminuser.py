from decouple import config
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates an admin user for the Django application."

    def handle(self, *args, **options):
        username = config("ADMIN_USER_NAME")
        email = config("ADMIN_USER_EMAIL")
        password = config("ADMIN_USER_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS("Admin user created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists."))
