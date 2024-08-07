import connection.conn as db
from data.constants import address
from utils.helpers import days_counter, remove_expired_items


def removeExpiredItemsCD(address:str, chain:str):

    connection_data = db.getConnectionData(address, chain)

    print(f"---------------{chain.upper()}---------------")
    days_counter(connection_data)
    connection_data_expired = remove_expired_items(connection_data, 30)
    
    db.removeExpiredConnectionData(connection_data_expired, chain)


if __name__ == '__main__':

    removeExpiredItemsCD(address, 'ethereum')
    removeExpiredItemsCD(address, 'blast')