from connection.conn import deleteList, insertList
from src.get_collections import read_from_google_sheets
from utils.helpers import retry


def updateCollections():

    collections = retry(read_from_google_sheets)
    if collections:
        retry(deleteList)
        retry(lambda: insertList(collections))


if __name__ == '__main__':

    updateCollections()