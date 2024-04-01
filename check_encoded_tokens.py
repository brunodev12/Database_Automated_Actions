import connection.conn as db
from utils.helpers import days_counter, remove_expired_items

if __name__ == '__main__':

    encodedTokens_data = db.getAllEncodedTokens()

    days_counter(encodedTokens_data)
    encodedTokens_expired = remove_expired_items(encodedTokens_data, 3)
    
    db.removeExpiredEncodedTokens(encodedTokens_expired)