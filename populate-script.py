import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventio.settings')
django.setup()

from accounts.models import User, Organisation
from meetings.models import Place,Meeting,Invitation

def populate():
    # Create an example organisation
    org, _ = Organisation.objects.get_or_create(
        name="Example Organisation"
    )


    place_data= [
        {"name": "Room 1", "location": "Building 1, Floor 2", "capacity": 10},
        {"name": "Room 2", "location": "Building 1, Floor 3", "capacity": 10},
        {"name": "Room 3", "location": "Building 2, Floor 3", "capacity": 20}
    ]

    for data in place_data:
        place, created = Place.objects.get_or_create(
            name=data["name"],
            defaults={
                "location": data["location"],
                "capacity": data["capacity"]
            }
        )
        if created:
            print(f"Created place: {place.name}")
        else:
            print(f"Place already exists: {place.name}")
    
    meeting_data=[
        {"description": "dfasfasd", "start_time": "2025-03-20 10:00:00", "end_time": "2025-03-20 12:00:00", "organiser_email":"alice@example.com","place_name":"Room 1"},
        {"description": "dfasfasd", "start_time": "2025-04-20 09:00:00", "end_time": "2025-04-20 10:00:00", "organiser_email":"alice@example.com","place_name":"Room 2"},
    ]

    for data in meeting_data:
        #for foreign keys
        organiser = User.objects.get(email=data["organiser_email"])
        place = Place.objects.get(name=data["place_name"])

        meeting,created=Meeting.objects.get_or_create(
            description=data["description"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            organiser=organiser,
            place=place
        )
    if created:
        print(f"Created meeting: {meeting.description}")
    else:
        print(f"Meeting already exists: {meeting.description}")


    invitation_data=[
        {"user_email": "alice@example.com", "meeting_id": 1, "status": True},
        {"user_email": "bob@example.com", "meeting_id": 2, "status": False},
    ]
    for data in invitation_data:
        user=User.objects.get(email=data["user_email"])
        meeting=Meeting.objects.get(meeting_id=data["meeting_id"])

        invitation, created = Invitation.objects.get_or_create(
        user=user,
        meeting=meeting,
        defaults={"status": data["status"]}
    )
    if created:
        print(f"Created invitation for {user.email} to {meeting.description}")
    else:
        print(f"Invitation already exists for {user.email} to {meeting.description}")
        

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