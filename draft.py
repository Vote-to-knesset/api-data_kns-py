from pymongo import MongoClient
from set_tables import *
from datetime import datetime
from dotenv import load_dotenv
import os
import datetime
load_dotenv()




client = MongoClient(os.environ.get('SECRET_MONGO'))
db = client['kns_data']
bills_collection = db['bills']
# parties_collection = db['parties']

bills = list(bills_collection.find({}, {'_id': 0}))
# parties = list(parties_collection.find({}, {'BillID': 1, '_id': 0}))
# bill_id_bills = [bill['BillID'] for bill in bills]
# bill_id_parties = set([bill['BillID'] for bill in parties])
print(bills)
for bill in bills:
    if bill['present'] == '':
        bill_id = bill['BillID']
        name = get_persona(bill_id)
        filter_criteria = {'BillID': bill_id}

        update_operation = {
            '$set': {
                'present': name,
            }
        }
        result = bills_collection.update_one(filter_criteria, update_operation)
        if result.matched_count > 0:
            print(f"Updated total_vote and in_favor for document with BillID: {bill_id}")







#
# for b in bill_id_bills:
#     if b not in bill_id_parties:
#         parties_data = {
#             "BillID": b,
#             "Likud_For": 0,
#             "Likud_Against": 0,
#             "YeshAtidNationalUnity_For": 0,
#             "YeshAtidNationalUnity_Against": 0,
#             "Shas_For": 0,
#             "Shas_Against": 0,
#             "Mafdal_ReligiousZionism_For": 0,
#             "Mafdal_ReligiousZionism_Against": 0,
#             "UnitedTorahJudaism_For": 0,
#             "UnitedTorahJudaism_Against": 0,
#             "OtzmaYehudit_For": 0,
#             "OtzmaYehudit_Against": 0,
#             "YisraelBeiteinu_For": 0,
#             "YisraelBeiteinu_Against": 0,
#             "UnitedArabList_For": 0,
#             "UnitedArabList_Against": 0,
#             "Hadash_Taal_For": 0,
#             "Hadash_Taal_Against": 0,
#             "LaborParty_For": 0,
#             "LaborParty_Against": 0,
#             "Noam_For": 0,
#             "Noam_Against": 0
#         }
#         parties_collection.insert_one(parties_data)
# print(bill_id_parties)
# print(bill_id_bills)


#
# import requests
#
# url = "https://www.knesset.gov.il/WebSiteApi/knessetapi/Votes/GetVoteDetails/"
#
# headers = {
#     "accept": "application/json, text/javascript, */*; q=0.01",
#     "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
#     "content-type": "application/json",
#     "if-none-match": "W/\"340ee0d3-ff84-43dd-a3e8-d01efc29903f\"",
#     "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "Referer": "https://main.knesset.gov.il/",
#     "Referrer-Policy": "strict-origin-when-cross-origin"
# }
#
#
#
# response = requests.get(url, headers=headers)
#
# if response.status_code == 200:
#     print(response.text)
# else:
#     print(f"Request failed with status code: {response.status_code}")


