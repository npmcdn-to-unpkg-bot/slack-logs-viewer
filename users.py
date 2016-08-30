import json
import os
from collections import namedtuple

User = namedtuple('User', ['id', 'name', 'real_name', 'avatar'])


def load_users(archive_location):
    users = json.load(open(os.path.join(archive_location, 'users.json')))
    users.append({'id': 'USLACKBOT', 'name': 'slackbot', 'real_name': '', 'avatar': ''})
    def avatar(u):
        if 'profile' in u:
            avatar = u['profile']['image_24']
        else:
            avatar = None
        return avatar
    return [User(id=u['id'], name=u['name'], real_name=u.get('real_name'), avatar=avatar(u)) for u in users]


users = load_users('/home/ether/sandbox/chat-analysis/ml2016/data')
def user_by_id(user_id):
    return filter(lambda u: u.id == user_id, users)[0]
