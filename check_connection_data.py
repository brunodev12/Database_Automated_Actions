import connection.conn as db
from utils.helpers import days_counter, remove_expired_items


def removeExpiredItemsCD(chain:str):

    connection_data = db.getConnectionData(chain)

    print(f"---------------{chain.upper()}---------------")
    days_counter(connection_data)
    connection_data_expired = remove_expired_items(connection_data, 30)
    
    db.removeExpiredConnectionData(connection_data_expired, chain)


if __name__ == '__main__':

    removeExpiredItemsCD('ethereum')
    removeExpiredItemsCD('blast')