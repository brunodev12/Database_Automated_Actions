from services.get_user_assets import getUserAssets
from services.token_events import getTokenEvents
import connection.conn as db
import os

address = os.environ.get("ADDRESS").upper()

tokenList_eth = getUserAssets(address, "ethereum")
tokenList_matic = getUserAssets(address, "matic")

tokenList = tokenList_eth + tokenList_matic

database_remote = db.readAllData(address)

'''Create local database'''

database_local = []

if tokenList:
    for i in tokenList:
        contract = i["contract"]
        token_id = i["tokenId"]
        chain = i["chain"]

        existing_item = None
        if database_remote:
            for item in database_remote:
                if (
                    item["contract"] == contract
                    and item["tokenId"] == token_id
                    and item["chain"] == chain
                    and item["owner"] == address
                ):
                    existing_item = item
                    break

        if existing_item:
            last_sale_price = existing_item.get("last_sale_price")
            id = existing_item.get("_id")
            i.update({"last_sale_price": last_sale_price, "_id": id})
        else:
            last_sale_price = getTokenEvents(chain, contract, token_id)
            i.update({"last_sale_price": last_sale_price})

        if i["last_sale_price"] == None:
            last_sale_price = getTokenEvents(chain, contract, token_id)
            i.update({"last_sale_price": last_sale_price})

        i.update({"owner": address})

    database_local = tokenList

'''Compare local and remote database'''

if database_remote:
    for local_element in database_local:
        if local_element not in database_remote:
            db.insertData(local_element)

    for remote_element in database_remote:
        if remote_element not in database_local:
            db.deleteData(remote_element)

    db.closeConnection()

else:
    db.createData(database_local)
    db.closeConnection()
