import connection.conn as db
from data.constants import address
from utils.helpers import days_counter, remove_expired_items


if __name__ == '__main__':

    connection_data = db.getConnectionData(address)

    days_counter(connection_data)
    connection_data_expired = remove_expired_items(connection_data, 30)
    
    db.removeExpiredConnectionData(connection_data_expired)
