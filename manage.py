from tools import ImportLogs
import sys

from settings import MONGO_DB


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'import':
        ImportLogs(MONGO_DB).import_archive(sys.argv[2])
    else:
        print 'bad command'
        print 'you can use "manage.py import <path-to-archive-dir>"'
