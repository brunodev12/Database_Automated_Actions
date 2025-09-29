import copy
import connection.conn as db
from src.get_user_assets import getUserAssets
from utils.last_price_utils import getLastSalePrice
from utils.helpers import sorted_list
from pymongo.errors import DuplicateKeyError
from data.constants import address, blockchains

print("test")
tokenList:list[dict] = []
for network in blockchains:
    contracts = getUserAssets(address, network)
    tokenList += contracts

database_remote:list[dict] = db.readAllData(address)

'''Create local database'''

database_local = []

if tokenList:

    for i in tokenList:
        number_token = 1
        contract = i["contract"]
        token_standard = i["tokenStandard"]
        if token_standard == 'erc1155':
            number_token = i["tokenNumber"]
        token_id = i["tokenId"]
        chain = i["chain"]

        existing_item = {}
        if database_remote:
            for item in database_remote:
                if (
                    item["contract"] == contract
                    and item["tokenId"] == token_id
                    and item["chain"] == chain
                    and item.get("tokenStandard") == token_standard
                    and item["owner"] == address
                    and item.get("tokenNumber") == number_token
                ):
                    existing_item = copy.copy(item)
                    break

        if existing_item:
            last_sale_price = existing_item.get("last_sale_price")
            token_number = existing_item.get("tokenNumber")
            date = existing_item.get("date")
            id = existing_item.get("_id")
            i.update({"last_sale_price": last_sale_price, "date": date, "tokenNumber": token_number, "_id": id})
        else:
            response = getLastSalePrice(chain, contract, token_id)
            if response:
                last_sale_price, date = response
            else:
                print(chain, contract, token_id)
                print("Response is None")
                last_sale_price = None
                date = "2023-11-18T07:37:47Z"
            i.update({"last_sale_price": last_sale_price, "date": date, "tokenNumber": number_token})

        i.update({"owner": address})

    database_local = tokenList

database_local = sorted_list(database_local)

'''Compare local and remote database'''

if database_remote:

    for remote_element in database_remote:
        if remote_element not in database_local:
            print("-------------------------Removing element-------------------------")
            print(remote_element['contract'], remote_element['tokenId'], remote_element['tokenStandard'],
                remote_element['chain'], remote_element['tokenNumber'], remote_element['last_sale_price'], remote_element['date'])
            db.deleteData(remote_element)

    for local_element in database_local:
        sale_price = local_element['last_sale_price']
        if local_element not in database_remote:
            print("-------------------------Adding element---------------------------")
            print(local_element['contract'], local_element['tokenId'], local_element['tokenStandard'],
                local_element['chain'], local_element['tokenNumber'], local_element['last_sale_price'], local_element['date'])
            try:
                db.insertData(local_element)
            except DuplicateKeyError:
                db.updateElement(local_element)

elif database_local:
    db.createData(database_local)

db.closeConnection()