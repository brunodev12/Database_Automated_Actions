from connection.conn import ensureUniqueKeyIndex, syncList, readList
from utils.access_token import getAccessToken
from utils.collections_stats_utils import checkCollectionStats
from utils.helpers import retry
from utils.set_workers_utils import setWorkers


if __name__ == '__main__':

    arbitrage_collections = readList()

    getAccessToken()

    arbitrage_collections = checkCollectionStats(arbitrage_collections)

    arbitrage_collections = setWorkers(arbitrage_collections)

    new_id = 1
    for item in arbitrage_collections:
        item['ID'] = str(new_id)
        volume_one_week = item.get("volume_one_week", 0.0)
        item['volume_one_week'] = str(volume_one_week)
        item.pop('_id', None)
        new_id += 1

    if arbitrage_collections:
        ensureUniqueKeyIndex("Arbitrage_Bidding_Bot", "Collection_Info")
        retry(lambda: syncList(arbitrage_collections, "Arbitrage_Bidding_Bot", "Collection_Info"))

