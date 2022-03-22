import os

HOST = '0.0.0.0'

PORT = 8088

FINOLOG_API_KEY = os.environ.get('API_KEY')

FINOLOG_BIZ_SETTINGS = [

    # Development
    {
        'biz_id': 25467, 'icon': 34346, 'goal_start': 0, 'goal_end': 26000, 'unit': 'k', 'duration': 50,
        'category_ids': 320912
    }
]
