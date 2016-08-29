from collections import namedtuple
import json
from datetime import datetime

User = namedtuple('User', ['id', 'name', 'real_name', 'avatar'])

class Message(namedtuple('Message', ['id', 'channel', 'ts', 'user', 'raw'])):
    @property
    def html(self):
        pass

    @property
    def text(self):
        pass

    def to_json(self):
        ret = self._asdict()
        ret['user'] = self.user._asdict()
        ret['ts'] = self.ts.isoformat()
        return ret


class MessagesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            obj = str(obj)
        else:
            return obj.__dict__
            #obj = super(MessagesEncoder, self).default(obj)
        return obj

    def encode(self, obj):
        return super(MessagesEncoder, self).encode(obj)

    def iterencode(self, obj, **kwargs):
        if isinstance(obj, tuple) and hasattr(obj, '_fields'):
            gen = self._iterencode_dict(obj.__dict__, markers)
        else:
            gen = super(MessagesEncoder, self).iterencode(obj, **kwargs)

        for chunk in gen:
            yield chunk
