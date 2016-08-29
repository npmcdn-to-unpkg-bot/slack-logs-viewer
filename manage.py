from tools import ImportLogs

from settings import MONGO_DB


if __name__ == '__main__':
    ImportLogs(MONGO_DB).import_archive('/home/ether/sandbox/chat-analysis/ml2016/data')
