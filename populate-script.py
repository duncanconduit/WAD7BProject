import os
import django
import random
from datetime import datetime, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventio.settings')
django.setup()

from django.utils import timezone
from accounts.models import User, Organisation
from meetings.models import Place, Meeting, Invitation

def clear_old_data():
    # Completely delete previous data
    print("Deleting old Invitations...")
    Invitation.objects.all().delete()
    print("Deleting old Meetings...")
    Meeting.objects.all().delete()
    print("Deleting old Places...")
    Place.objects.all().delete()
    print("Deleting old Users...")
    User.objects.all().delete()
    print("Deleting old Organisations...")
    Organisation.objects.all().delete()

def create_organisations():
    org_names = ["Alpha Corp", "Beta Limited", "Gamma Enterprises"]
    org_objects = {}
    for name in org_names:
        # Create new organisation since old data has been removed
        org = Organisation.objects.create(name=name)
        org_objects[name] = org
        print(f"Created organisation: {org.name}")
    return org_objects

def create_users(org_objects):
    users = []
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Ian", "Julia",
                   "Kevin", "Laura", "Michael", "Nina", "Oliver", "Paula", "Quentin", "Rachel", "Steven", "Tina",
                   "Umar", "Victoria", "Walter", "Xenia", "Yannick", "Zoe", "Aaron", "Beatrice", "Caleb", "Deborah",
                   "Ethan", "Faith", "Gavin", "Helena", "Isaac", "Jasmine", "Kyle", "Lara", "Martin", "Nora",
                   "Owen", "Penny", "Quincy", "Rita", "Samuel", "Teresa", "Ulysses", "Valerie", "Wendy", "Xander"]

    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                  "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
                  "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall",
                  "Young", "Allen", "Sanchez", "Wright", "King", "Scott", "Green", "Baker", "Adams", "Nelson",
                  "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter", "Phillips", "Evans", "Turner", "Torres"]

    total_users = 50
    org_names = list(org_objects.keys())
    for i in range(total_users):
        # Distribute users evenly by choosing an organisation via round robin:
        org_name = org_names[i % len(org_names)]
        org = org_objects[org_name]
        first_name = first_names[i % len(first_names)]
        last_name = last_names[i % len(last_names)]
        email = f"user{i+1}@example.com"
        user = User.objects.create(email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   organisation=org)
        user.set_password("defaultpassword")
        user.save()
        users.append(user)
        print(f"Created user: {user.email} assigned to {org.name}")
    return users

def create_places():
    places_data = [
        {"name": "Conference Room A", "address": "Main Building, Floor 1", "capacity": 20},
        {"name": "Conference Room B", "address": "Main Building, Floor 2", "capacity": 15},
        {"name": "Meeting Room 1", "address": "Annex Building, Floor 1", "capacity": 10},
        {"name": "Meeting Room 2", "address": "Annex Building, Floor 2", "capacity": 12},
        {"name": "Board Room", "address": "Executive Wing, Floor 3", "capacity": 8},
        {"name": "Training Room", "address": "Learning Centre, Floor 1", "capacity": 25},
        {"name": "Seminar Hall", "address": "Convention Centre, Ground Floor", "capacity": 40},
        {"name": "Strategy Room", "address": "Main Building, Floor 3", "capacity": 10},
        {"name": "Huddle Room", "address": "Open Office, Floor 1", "capacity": 6},
        {"name": "Open Space", "address": "Rooftop", "capacity": 30},
    ]

    places = {}
    for data in places_data:
        place = Place.objects.create(
            name=data["name"],
            address=data["address"],
            capacity=data["capacity"]
            # latitude and longitude are optional and default to None
        )
        places[place.name] = place
        print(f"Created place: {place.name}")
    return places

def random_business_datetime(min_offset=timedelta(hours=1), max_offset=timedelta(weeks=2)):
    """
    Returns a datetime between now+min_offset and now+max_offset with a time adjusted to be within business hours (9am-17:00).
    """
    now = timezone.now()
    # Choose a random timedelta between the given range in seconds.
    total_seconds = (max_offset - min_offset).total_seconds()
    random_seconds = random.randint(0, int(total_seconds))
    random_datetime = now + min_offset + timedelta(seconds=random_seconds)
    
    # Adjust to business hours:
    business_start = time(9, 0, 0)
    business_end = time(17, 0, 0)
    
    # If the random time is before business hours, move it up; if after, set to beginning of next business day.
    if random_datetime.time() < business_start:
        random_datetime = random_datetime.replace(hour=9, minute=0, second=0, microsecond=0)
    elif random_datetime.time() > business_end:
        # move to next day at 9 AM
        random_datetime = (random_datetime + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    return random_datetime

def create_meetings(users, places):
    meeting_objects = {}
    total_meetings = 30
    meeting_descriptions = [f"Meeting {i+1}" for i in range(total_meetings)]
    place_list = list(places.values())
    
    for desc in meeting_descriptions:
        # Randomly choose an organiser from the user list.
        organiser = random.choice(users)
        
        # Create a meeting start time that is within business hours between 1 hour and 2 weeks in the future.
        start_datetime = random_business_datetime()
        # Randomly select a meeting duration of 30 mins, 45 mins, or 60 mins.
        duration = random.choice([30, 45, 60])
        end_datetime = start_datetime + timedelta(minutes=duration)
        
        # Ensure the end time is still within business hours.
        if end_datetime.time() > time(17, 0, 0):
            # If not, adjust the meeting duration so that it ends at or before 17:00.
            end_datetime = start_datetime.replace(hour=17, minute=0, second=0, microsecond=0)
        
        # Randomly choose a meeting place.
        place = random.choice(place_list)
        
        meeting = Meeting.objects.create(
            description=desc,
            start_time=start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            end_time=end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            organiser=organiser,
            place=place
        )
        meeting_objects[desc] = meeting
        print(f"Created meeting: {meeting.description} organised by {organiser.email} at {place.name}")
    return meeting_objects

def create_invitations(users, meeting_objects):
    # For each meeting, invite a random subset (*at least 3 attendees*) of users (excluding the organiser)
    for meeting in meeting_objects.values():
        # Filter out organiser from potential invitees
        potential_invitees = [user for user in users if user != meeting.organiser]
        # Random number of invitees chosen between 3 and min(total, 15)
        num_invitees = random.randint(3, min(15, len(potential_invitees)))
        invitees = random.sample(potential_invitees, num_invitees)
        
        for user in invitees:
            # status can be one of: True (accepted), False (declined), or None (pending)
            status = random.choice([True, False, None])
            Invitation.objects.create(
                user=user,
                meeting=meeting,
                status=status
            )
            print(f"Invited user {user.email} to meeting {meeting.description} (Status: {status})")

def populate():
    org_objects = create_organisations()
    users = create_users(org_objects)
    places = create_places()
    meeting_objects = create_meetings(users, places)
    create_invitations(users, meeting_objects)
    
if __name__ == '__main__':
    populate()