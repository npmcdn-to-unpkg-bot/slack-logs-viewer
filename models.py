from collections import namedtuple
import json
import re
from datetime import datetime

from users import user_by_id


class Message(namedtuple('Message', ['id', 'channel', 'ts', 'user', 'raw'])):
    @property
    def html(self):
        pass

    @property
    def text(self):
        pass

    @property
    def prerender(self):
        user_re = r'<@(?P<USER>\w+)>'
        return re.sub(user_re, lambda x: '<@%s|@%s>' % (x.group(1), user_by_id(x.group(1)).name), self.raw)

    def to_json(self):
        ret = self._asdict()
        ret['user'] = self.user._asdict()
        ret['ts'] = self.ts.isoformat()
        ret['text'] = self.prerender
        del ret['raw']
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
