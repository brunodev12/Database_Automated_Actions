from datetime import datetime

def date_to_timestamp(date):

    date_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    timestamp = date_datetime.timestamp()

    return int(timestamp)

def sorted_list(unordered_list = []):

    for item in unordered_list:
        if item["last_sale_price"] is None:
            item["last_sale_price"] = 0

    sorted_data = sorted(unordered_list, key=lambda x: (x["contract"], x["tokenId"], x["tokenStandard"], -x["last_sale_price"]))

    current_key = None
    current_number = 0

    for item in sorted_data:
        key = (item["contract"], item["tokenId"], item["tokenStandard"])
        
        if key != current_key:
            current_key = key
            current_number = 1
        else:
            current_number += 1
        
        item["tokenNumber"] = current_number

        if item["last_sale_price"] == 0:
            item["last_sale_price"] = None
    
    return sorted_data