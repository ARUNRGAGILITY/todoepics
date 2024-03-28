# create_user_groups.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_djangobase.settings")
django.setup()

from django.contrib.auth.models import Group

def create_user_groups():
    group_names = ['team_member', 'scrum_master', 'product_owner', 'project_admin', 'site_admin', 'stakeholders', 'consumers']

    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"Group '{group.name}' created.")
        else:
            print(f"Group '{group.name}' already exists.")

if __name__ == "__main__":
    create_user_groups()
