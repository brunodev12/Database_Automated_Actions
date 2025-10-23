from connection.conn import deleteList
from utils.helpers import retry


def updateCollections():

    retry(lambda: deleteList("Arbitrage_Bidding_Bot", "Collection_Info"))


if __name__ == '__main__':

    updateCollections()