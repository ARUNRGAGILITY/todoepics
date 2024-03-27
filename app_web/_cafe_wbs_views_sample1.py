def cafe_wbs(request):
    hierarchy = {
    'StrategicTheme': {
        'name': 'ST1',
        'Epics': [
            {
                'name': 'E1',
                'Features': [
                    {
                        'name': 'F1',
                        'UserStories': [
                            {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                        ]
                    },
                    {
                        'name': 'F2',
                        'UserStories': [
                            {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                        ]
                    },
                    {
                        'name': 'F3',
                        'UserStories': [
                            {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                            {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                        ]
                    }
                ]
                        },
                        {
                            'name': 'E2',
                            'Features': [
                                {
                                    'name': 'F1',
                                    'UserStories': [
                                        {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                                    ]
                                },
                                {
                                    'name': 'F2',
                                    'UserStories': [
                                        {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                                    ]
                                },
                                {
                                    'name': 'F3',
                                    'UserStories': [
                                        {'name': 'US1', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US2', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]},
                                        {'name': 'US3', 'Tasks': [{'name': 'Task1'}, {'name': 'Task2'}, {'name': 'Task3'}, {'name': 'Task4'}]}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
    context = {'hierarchy': hierarchy}
    
    template_file = f"{app_name}/_cafe/mgmt/cafe_wbs.html"
    return render(request, template_file, context)
