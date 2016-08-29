# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from collections import namedtuple

from pymongo import MongoClient
from bson.objectid import ObjectId

from models import Message, User


db = MongoClient().slacklogs
messageslist = db.messages


def messages_deco(func):
    def inner(*args, **kwargs):
        return mongo_to_messages(func(*args, **kwargs))
    return inner


class LogQuery:
    def __init__(self):  
        self._filters = {}
        self._sort = None
        self._limit = None
        self._neighbors = 0

    def search(self, text):
        self._filters['$text'] = {'$search': text}
        return self

    def filter(self, param_or_dict, value=None):
        if type(param_or_dict) == dict and not value:
            self._filters.update(param_or_dict)
        elif type(param_or_dict) == str:
            self._filters[param_or_dict] = value
        else:
            raise Exception('param_or_dict must be string or dict')

        return self

    def asc(self):
        self._sort = 1
        return self

    def desc(self):
        self._sort = -1
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def channel(self, name):
        return self.filter('channel', name)

    def before_message(self, message_id):
        self._filters['_id'] = {'$lt': message_id}
        return self

    def neighbors(self, num):
        self._neighbors = num
        return self

    def _add_neighbor(self, message_id):
        count = self._neighbors
        message_id = ObjectId(message_id)
        " get count messages before and above this message "
        before = messageslist.find({'_id':  {'$lt': message_id}}).sort([('_id', -1)]).limit(count)
        message = messageslist.find({'_id': message_id})
        after = messageslist.find({'_id':  {'$gt': message_id}}).sort('_id').limit(count)
        return mongo_to_messages(before) + mongo_to_messages(message) +  mongo_to_messages(after)

    def _add_neighbors(self, result):
        ret = []
        for r in result:
            ret.append(self._add_neighbor(r['_id']))
        return ret

    def get(self):
        result = messageslist.find(self._filters)
        if self._sort is not None:
            result = result.sort('$natural', self._sort)
        if self._limit:
            result = result.limit(self._limit)
        if self._neighbors:
            result = self._add_neighbors(result)
        return result


class LogViewer:
    @messages_deco
    def search(self, text, channel=None, author=None, period=None):
        return LogQuery().search(text).get()
    def search_with_neighbors(self, text):
        return LogQuery().search(text).neighbors(3).get()
    def by_period(self, period):
        pass
    def head(self, message_ts, length=100):
        " first length messages from message_ts message "
        pass
    @messages_deco
    def tail(self, channel, length=10, before_message=None):
        ret = LogQuery().channel(channel)
        if before_message:
            ret = ret.before_message(before_message)
        return ret.desc().limit(length).get()


def mongo_to_messages(mongo_result):
    def mtom(m):
        return Message(id=str(m['_id']), channel=m['channel'], ts=m['ts'], user=user_by_id(m['user']), raw=m['text'])
    return map(mtom, mongo_result)


def load_users(archive_location):
    users = json.load(open(os.path.join(archive_location, 'users.json')))
    #return [User(id=u['id'], name=u['name'], real_name=u['real_name']) for u in users]
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


if __name__ == '__main__':
#    import_logs('/home/ether/sandbox/chat-analysis/ml2016/data')
    lv = LogViewer()
    # msgs = lv.tail('random')
    #msgs = lv.neighbors('57c06ab13b80a11fbf25b46d')
    """
    msgs = lv.search('SLACKBOT')
    for m in msgs:
        print '%s [%s] %s: %s' % (m.id, m.ts, m.user.name, m.text)
    """
    msgs = lv.search_with_neighbors(u'видеоигры')
    for g in msgs:
        for m in g:
            print '[%s] %s: %s' % (m.ts, m.user.name, m.text)
        print('')

    
