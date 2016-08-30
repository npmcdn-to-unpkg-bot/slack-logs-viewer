# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from collections import namedtuple

from pymongo import MongoClient

from models import Message
from users import user_by_id


db = MongoClient().slacklogs
messageslist = db.messages


def mongo_to_messages(mongo_result):
    def mtom(m):
        return Message(id=m['id'], channel=m['channel'], ts=m['ts'], user=user_by_id(m['user']), raw=m['text'])
    return map(mtom, mongo_result)


def to_message_list(func):
    def inner(*args, **kwargs):
        return mongo_to_messages(func(*args, **kwargs))
    return inner


class LogQuery:
    def __init__(self):  
        self._filters = {'subtype': {'$exists': False}}
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
        self._filters['id'] = {'$lt': int(message_id)}
        return self

    def neighbors(self, num):
        self._neighbors = num
        return self

    def _add_neighbor(self, message_id):
        count = self._neighbors
        message_id = message_id
        " get count messages before and above this message "
        before = messageslist.find({'id':  {'$lt': message_id}}).sort([('id', -1)]).limit(count)
        message = messageslist.find({'id': message_id})
        after = messageslist.find({'id':  {'$gt': message_id}}).sort('id').limit(count)
        return mongo_to_messages(before) + mongo_to_messages(message) +  mongo_to_messages(after)

    def _add_neighbors(self, result):
        ret = []
        for r in result:
            ret.append(self._add_neighbor(r['id']))
        return ret

    def get(self):
        result = messageslist.find(self._filters)
        if self._sort is not None:
            result = result.sort('id', self._sort)
        if self._limit:
            result = result.limit(self._limit)
        result = sorted(result, key=lambda x: x['id'])
        if self._neighbors:
            result = self._add_neighbors(result)
        return result


class LogViewer:
    @to_message_list
    def search(self, text, channel=None, author=None, period=None):
        return LogQuery().search(text).get()

    def search_with_neighbors(self, text):
        return LogQuery().search(text).neighbors(3).get()

    @to_message_list
    def tail(self, channel, length=10, before_message=None):
        ret = LogQuery().channel(channel)
        if before_message:
            ret = ret.before_message(before_message)
        return ret.desc().limit(length).get()
