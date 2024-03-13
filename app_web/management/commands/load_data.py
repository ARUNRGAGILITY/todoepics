from django.core.management.base import BaseCommand
import json
from app_web.models import *
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Loads data from a JSON file into the database.'

    def handle(self, *args, **kwargs):
        # Adjust the file path as necessary
        with open('./input_load_data/st_input.json', 'r') as file:
            data = json.load(file)
            
            for theme_data in data:
                theme = StrategicTheme.objects.create(
                    name=theme_data['name'],
                    description=theme_data['description'],
                    # Assuming all themes are active and a default author
                    active=True,
                )
                for objective_data in theme_data['objectives']:
                    objective = Objective.objects.create(
                        theme=theme,
                        title=objective_data['title'],
                        description=objective_data['description'],
                        active=True,
                    )
                    for kr_data in objective_data['key_results']:
                        kr = KeyResult.objects.create(
                            objective=objective,
                            name=kr_data['name'],
                            target=kr_data['target'],
                            active=True,
                        )
                        for qm_data in kr_data['quarterly_measures']:
                            QuarterlyMeasure.objects.create(
                                key_result=kr,
                                quarter=qm_data['quarter'],
                                year=qm_data['year'],
                                percentage=qm_data['value'],
                                active=True,
                            )
        self.stdout.write(self.style.SUCCESS('Successfully loaded strategic themes and related data.'))
