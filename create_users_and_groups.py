# create_users_and_groups.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_djangobase.settings")
django.setup()

from django.contrib.auth.models import User, Group


def create_user(username, email, password, first_name, last_name, groups):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    if created:
        user.set_password(password)
        user.save()
        for group_name in groups:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        print(f"User {username} created and added to groups: {', '.join(groups)}")
    else:
        print(f"User {username} already exists.")

def main():
    # Create users and assign to groups
    create_user("team_member1", "team_member1@example.com", "password123", "Team", "Member1", ["team_member"])
    create_user("scrum_master1", "scrum_master1@example.com", "password123", "Scrum", "Master1", ["scrum_master"])
    create_user("product_owner1", "product_owner1@example.com", "password123", "Product", "Owner1", ["product_owner"])
    create_user("project_admin1", "project_admin1@example.com", "password123", "Project", "Admin1", ["project_admin"])
    create_user("site_admin1", "site_admin1@example.com", "password123", "Site", "Admin1", ["site_admin"])
    create_user("stakeholder1", "stakeholder1@example.com", "password123", "Stake", "Holder1", ["stakeholders"])
    create_user("consumer1", "consumer1@example.com", "password123", "Consumer", "Customer1", ["consumers"])


if __name__ == "__main__":
    main()
