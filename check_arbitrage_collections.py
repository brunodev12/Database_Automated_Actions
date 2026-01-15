from connection.conn import deleteList, insertList, readList
from utils.access_token import getAccessToken
from utils.collections_stats_utils import checkCollectionStats
from utils.helpers import retry
from utils.set_workers_utils import setWorkers


if __name__ == '__main__':

    arbitrage_collections = readList()

    getAccessToken()

    arbitrage_collections = checkCollectionStats(arbitrage_collections)

    arbitrage_collections = setWorkers(arbitrage_collections)

    for item in arbitrage_collections:
        volume_one_week = item.get("volume_one_week", 0.0)
        item['volume_one_week'] = str(volume_one_week)
        item.pop('_id', None)

    if arbitrage_collections:
        retry(lambda: deleteList("Arbitrage_Bidding_Bot", "Collection_Info"))
        retry(lambda: insertList(arbitrage_collections, "Arbitrage_Bidding_Bot", "Collection_Info"))

