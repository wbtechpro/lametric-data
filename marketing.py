import json


def marketing_recruiting(values):
    data = []
    icon = 39441
    for item in values:
        if isinstance(item, list):
            for obj, value in item:
                data.append({'text': '{} {}'.format(obj, value), 'icon': icon})
                icon += 1
        elif isinstance(item, dict):
            for key, value in item.items():
                data.append({'text': '{}'.format(key), 'icon': icon})
                icon += 1
                for i, x in value:
                    data.append({'text': '{} {}'.format(i, x)})
    return json.dumps(dict(frames=data))
