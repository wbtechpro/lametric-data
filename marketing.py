import json


def marketing_recruiting(values, goals):
    data = []
    keys = list(*values.keys())
    data.append({'text': keys[0], 'icon': (icon := keys[1])})
    for item in values[(*keys,)]:
        if isinstance(item, tuple):
            data.append({"goalData": {"start": 0,
                                      "current": item[1],
                                      "end": goals[item[0]],
                                      "unit": item[0]},
                         'icon': icon})
        elif isinstance(item, dict):
            for key, value in item.items():
                data.append({'text': '{}:'.format(key), 'icon': icon})
                for i, x in value:
                    data.append({"goalData": {"start": 0,
                                              "current": x,
                                              "end": goals[i],
                                              "unit": i}, 'icon': icon})
    return json.dumps(dict(frames=data), ensure_ascii=False)
