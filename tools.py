import os
import json
from datetime import datetime

from pymongo import MongoClient

# TODO: .zip support

def prepare_message(message, channel):
    message['id'] = int(message['ts'].replace('.', ''))
    message['ts'] = datetime.fromtimestamp(float(message['ts']))
    message['channel'] = channel
    return message

class ImportLogs:
    def __init__(self, db_name):
        self.messages = MongoClient()[db_name].messages

    def import_archive(self, archive_location):
        for f in os.listdir(archive_location):
            if os.path.isdir(os.path.join(archive_location, f)):
                self.import_channel(archive_location, f)

    def update_from_archive(self):
        raise NotImplementedError()

    def import_channel(self, archive_location, name):
        if '/' in name:
            raise Exception('channel name cannot include slashes')
        channel_loc = os.path.join(archive_location, name)
        listing = os.listdir(channel_loc)
        messages_count = 0
        for f in listing:
            with open(os.path.join(channel_loc, f)) as dayfile:
                content = json.load(dayfile)
                messages_count += len(content)
                self.messages.insert_many([prepare_message(m, name) for m in content])
        print 'channel %s, days: %s, messages: %s' % (name, len(listing), messages_count)
