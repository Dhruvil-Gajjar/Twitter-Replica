import random

from DB import client
from Auth import db, request_user


def get_users_list():
    all_users = db.child("users").get()

    users_list = []
    for user in all_users.each():
        if request_user.get('uid') != user.item[0]:
            users_list.append({
                "user_id": user.item[0],
                "user_name": user.item[1].get("name", "")
            })

    return users_list


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


def get_all_tweets(entity_kind):
    query = client.query(kind=entity_kind)
    results = list(query.fetch())

    data = list()
    for obj in results:
        data_dict = dict()
        for key, value in obj.items():
                data_dict[key] = value

        data.append(data_dict)

    for obj in data:
        if obj.get("post_id"):
            continue
        else:
            data.remove(obj)

    return data


def get_tweets(entity_kind):
    data = list()
    user_tweets = get_all_tweets(entity_kind)
    data.extend(user_tweets)

    user_data = get_profile_details(entity_kind)
    for obj in user_data.get("following"):
        following_tweets = get_all_tweets(obj.get("user_id"))
        data.extend(following_tweets)

    final_data = list(filter(None, data))
    random.shuffle(final_data)
    return final_data


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


def get_followings(user_id):
    data = get_entities(user_id)

    for obj in data:
        if obj.get("profile") == True:
            return obj.get("following")
        
        
def get_followers(user_id):
    data = get_entities(user_id)

    for obj in data:
        if obj.get("profile") == True:
            return obj.get("followers")
