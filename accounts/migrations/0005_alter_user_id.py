from django.db import migrations
import uuid

def set_unique_user_ids(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        user.id = uuid.uuid4()
        user.save(update_fields=['id'])

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_avatar_colour'),
    ]

    operations = [
        migrations.RunPython(set_unique_user_ids),
    ]