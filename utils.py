from DB import client
from Auth import request_user


def get_entities(entity_kind):
    query = client.query(kind=entity_kind)
    results = list(query.fetch())

    data = list()
    for obj in results:
        data_dict = dict()
        for key, value in obj.items():
            data_dict[key] = value

        data.append(data_dict)

    return list(filter(None, data))


def get_post_details(post_id):
    data = get_entities(request_user["uid"])

    for obj in data:
        if obj.get("post_id") == post_id:
            return obj


def get_profile_details(user_id):
    data = get_entities(user_id)

    for obj in data:
        if obj.get("profile") == True:
            return obj
