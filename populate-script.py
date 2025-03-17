import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventio.settings')
django.setup()

from accounts.models import User, Organisation

def populate():
    # Create an example organisation
    org, _ = Organisation.objects.get_or_create(
        name="Example Organisation"
    )

    # Create some sample users
    user_data = [
        {"email": "alice@example.com", "first_name": "Alice", "last_name": "Smith", "password": "testpassword123"},
        {"email": "bob@example.com", "first_name": "Bob", "last_name": "Johnson", "password": "testpassword456"},
        {"email": "charlie@example.com", "first_name": "Charlie", "last_name": "Brown", "password": "testpassword789"}
    ]

    for data in user_data:
        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "organisation": org
            }
        )
        if created:
            user.set_password(data["password"])
            user.save()
            print(f"Created user: {user.email}")
        else:
            print(f"User already exists: {user.email}")

if __name__ == '__main__':
    populate()