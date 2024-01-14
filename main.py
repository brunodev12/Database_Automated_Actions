from services.get_user_assets import getUserAssets
from services.token_events import getTokenEvents
from utils.helpers import sorted_list
import connection.conn as db
from data.constants import address
import copy

tokenList_eth = getUserAssets(address, "ethereum")
tokenList_matic = getUserAssets(address, "matic")

tokenList = tokenList_eth + tokenList_matic

database_remote = db.readAllData(address)

'''Create local database'''

database_local = []

if tokenList:

    previous_contract = ''
    previous_token_id = ''
    previous_chain = ''
    previous_token_standard = ''

    request_counter = 1
    same_token = False

    for index,i in enumerate(tokenList):
        number_token = 1
        contract = i["contract"]
        token_standard = i["tokenStandard"]
        if token_standard == 'erc1155':
            number_token = i["tokenNumber"]
        token_id = i["tokenId"]
        chain = i["chain"]

        if index>0:
            previous_contract = tokenList[index-1]['contract']
            previous_token_id = tokenList[index-1]['tokenId']
            previous_chain = tokenList[index-1]['chain']
            previous_token_standard = tokenList[index-1]['tokenStandard']
        
        if (
            contract == previous_contract
            and token_id == previous_token_id
            and chain == previous_chain
            and token_standard == previous_token_standard
            ):
            same_token = True
        else:
            same_token = False

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
            if not same_token:
                request_counter = 1
            response = getTokenEvents(chain, contract, token_id, request_counter)
            if response:
                last_sale_price, date = response
                if same_token:
                    request_counter += 1
            else:
                print(chain, contract, token_id, request_counter)
                print("Response is None")
                last_sale_price = None
                date = "2023-11-18T07:37:47Z"
            i.update({"last_sale_price": last_sale_price, "date": date, "tokenNumber": number_token})

        i.update({"owner": address})

    database_local = tokenList

database_local = sorted_list(database_local)

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