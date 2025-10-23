from connection.conn import readList
from src.get_collections import upload_to_google_sheets
from datetime import datetime, timezone
from utils.helpers import retry


def upload_collections():

    collections:list[dict] = readList()

    utc_time = datetime.now(timezone.utc)

    formatted_time = utc_time.strftime("%Y-%m-%d %H:%M:%S")
    for item in collections:
        item.pop('_id', None)
        item['last_update_db'] = formatted_time
    
    retry(lambda: upload_to_google_sheets(collections))


if __name__ == '__main__':

    upload_collections()