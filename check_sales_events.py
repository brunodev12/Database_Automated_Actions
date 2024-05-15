import time
import copy
from utils.clear_variables import clearGlobalVariables
from utils.collections_utils import getCollectionsUtils
from utils.db_data_utils import getSalesEventsDB, saveAllDataDB
from utils.helpers import daysStats, getAveragePrice, remove_expired_items_2
from utils.sales_events_utils import getSalesEventsUtils
from data.variables import token_price, elements_stats_for_DB, sales_events_global

def run():

    getSalesEventsDB()

    collections = getCollectionsUtils()
    time_now = int(time.time())

    all_elements_stats = elements_stats_for_DB['all_elements_stats']

    for index, item in enumerate(collections):
        collection_events = []
        index_value = max(0, index - 1)
        slug = str(item['slug'])
        previous_slug = str(collections[index_value]['slug'])
        contract = str(item['contract'])
        chain = str(item['chain'])
        trait_type = str(item['type'])
        trait_value = str(item['value'])
        asset = str(item['assets'])
        print("===================================")
        print(slug, contract, chain, trait_type, trait_value, asset)
        collection_events, last_update = getSalesEventsUtils(slug, contract, chain, time_now, trait_type, trait_value, asset)
        average_one_day, one_sales, buys_one_day, sales_one_day  = getAveragePrice(collection_events, token_price, 1, time_now)
        average_seven_days, seven_sales, buys_seven_days, sales_seven_days = getAveragePrice(collection_events, token_price, 7, time_now)
        average_thirty_days, thirty_sales, buys_thirty_day, sales_thirty_days = getAveragePrice(collection_events, token_price, 30, time_now)
        print("AVERAGE ONE DAY ->", round(average_one_day, 6), "|TOTAL SALES ONE DAY ->", one_sales, "|BUYS ONE DAY ->", buys_one_day, "|SALES ONE DAY ->", sales_one_day)
        print("AVERAGE SEVEN DAYS ->", round(average_seven_days, 6), "|TOTAL SALES SEVEN DAYS ->", seven_sales, "|BUYS SEVEN DAYS ->", buys_seven_days, "|SALES SEVEN DAYS ->", sales_seven_days)
        print("AVERAGE THIRTY DAYS ->", round(average_thirty_days, 6), "|TOTAL SALES THIRTY DAYS ->", thirty_sales, "|BUYS THIRTY DAYS ->", buys_thirty_day, "|SALES THIRTY DAYS ->", sales_thirty_days)


        if slug != previous_slug:
            clearGlobalVariables()
        

        one_day_stats = daysStats(buys_one_day, sales_one_day, one_sales, average_one_day)

        seven_days_stats = daysStats(buys_seven_days, sales_seven_days, seven_sales, average_seven_days)

        thirty_days_stats = daysStats(buys_thirty_day, sales_thirty_days, thirty_sales, average_thirty_days)

        stats = {
            'one_day': one_day_stats,
            'seven_days': seven_days_stats,
            'thirty_days': thirty_days_stats
        }

        stats_unique = copy.copy(stats)
        
        element_stats = {
            'slug': slug,
            'contract': contract,
            'chain': chain,
            'asset': asset,
            'trait_type': trait_type,
            'trait_value': trait_value,
            'last_update': last_update,
            'stats': stats_unique
        }

        unique_element_stats = copy.copy(element_stats)
        all_elements_stats.append(unique_element_stats)

    all_sales_events = sales_events_global['allSalesEvents']
    all_sales_events = remove_expired_items_2(all_sales_events, 7)
    sales_events_global['allSalesEvents'] = all_sales_events

    saveAllDataDB()


if __name__ == '__main__':

    run()