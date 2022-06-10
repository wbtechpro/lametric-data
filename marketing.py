import json


def marketing_recruiting(values, goals_emoji):
    data = []
    keys = list(*values.keys())
    data.append({'text': keys[0], 'icon': (icon := keys[1])})
    for item in values[(*keys,)]:
        if isinstance(item, tuple):
            data.append({"goalData": {"start": 0,
                                      "current": item[1],
                                      "end": goals_emoji[item[0]][0],
                                      "unit": ' {}'.format(goals_emoji[item[0]][1])},
                         'icon': icon})
        elif isinstance(item, dict):
            for key, value in item.items():
                data.append({'text': '{}:'.format(key), 'icon': icon})
                for i, x in value:
                    data.append({"goalData": {"start": 0,
                                              "current": x,
                                              "end": goals_emoji[i][0],
                                              "unit": ' {}'.format(goals_emoji[i][1])}, 'icon': icon})
    return json.dumps(dict(frames=data), ensure_ascii=False)
