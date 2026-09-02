from connection.conn import ensureUniqueKeyIndex, syncList
from src.get_collections import read_from_google_sheets
from utils.helpers import retry


def updateCollections():

    collections = retry(lambda: read_from_google_sheets("Arbitrage - Collections", "Collections"))
    if collections:
        ensureUniqueKeyIndex("Arbitrage_Bidding_Bot", "Collection_Info")
        retry(lambda: syncList(collections, "Arbitrage_Bidding_Bot", "Collection_Info"))

if __name__ == '__main__':

    updateCollections()