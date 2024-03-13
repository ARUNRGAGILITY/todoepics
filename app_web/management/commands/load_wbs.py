# run this from the project directory
from django.core.management.base import BaseCommand
import json
from django.contrib.auth.models import User
from app_web.models import StrategicTheme, Epic, Feature, Capability, UserStory, Spike, Task

class Command(BaseCommand):
    help = 'Loads data from a JSON file into the database, linking items to an existing Strategic Theme.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing the data.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as file:
            data = json.load(file)

            for item in data:
                # Fetch the Strategic Theme by ID
                try:
                    strategic_theme = StrategicTheme.objects.get(id=item["strategic_theme_id"])
                except StrategicTheme.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Strategic Theme with ID {item["strategic_theme_id"]} does not exist.'))
                    continue

                for epic_data in item.get('epics', []):
                    epic = Epic.objects.create(
                        name=epic_data['name'],
                        description=epic_data['description'],
                        type=epic_data['type'],
                        theme=strategic_theme,
                    )

                    for feature_data in epic_data.get('features', []):
                        feature = Feature.objects.create(
                            epic=epic,
                            name=feature_data['name'],
                            description=feature_data['description'],
                            type=feature_data['type'],
                        )

                        for story_data in feature_data.get('user_stories', []):
                            user_story = UserStory.objects.create(
                                parent_feature=feature,
                                name=story_data['name'],
                                description=story_data['description'],
                            )

                            for task_data in story_data.get('tasks', []):
                                Task.objects.create(
                                    parent_story=user_story,
                                    name=task_data['name'],
                                    description=task_data['description'],
                                )

                    for capability_data in epic_data.get('capabilities', []):
                        capability = Capability.objects.create(
                            epic=epic,
                            name=capability_data['name'],
                            description=capability_data['description'],
                            type=capability_data['type'],
                        )

                        for spike_data in capability_data.get('spikes', []):
                            spike = Spike.objects.create(
                                parent_capability=capability,
                                name=spike_data['name'],
                                description=spike_data['description'],
                            )

                            for task_data in spike_data.get('tasks', []):
                                Task.objects.create(
                                    parent_spike=spike,
                                    name=task_data['name'],
                                    description=task_data['description'],
                                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded all data.'))
