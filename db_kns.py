from set_tables import *
import threading
import time
from pymongo import MongoClient, DESCENDING

import os

SECRET_MONGO = os.getenv('SECRET_MONGO')


client = MongoClient(SECRET_MONGO)
db = client['kns_data']

bills_collection = db['bills']


sorted_bills = list(bills_collection.find({}, {'_id': 0}))
new_last = int(sorted_bills[-1]['BillID'])



def update_new_bills():
    global new_last
    new_data = knesset_data_info.get_bills(25, new_last)
    if len(new_data) > 0:
        new_last = new_data[-1]['BillID']
        new_table(new_data)

def new_table(new_data):
    filter_bills_1 = information(new_data)
    bills_plus_document_1 = get_documents(filter_bills_1)
    finished_table_1 = get_billi(bills_plus_document_1)
    for votes in finished_table_1:
        votes['total_vote'] = 0
        votes['in_favor'] = 0
        votes['against'] = 0
    add_toMongo(finished_table_1)

def add_toMongo(finished_table_1):
    bills_collection = db['bills']
    parties_collection = db['parties']

    for bill in finished_table_1:
        try:
            bill_data = {
                'BillID': bill['BillID'],
                'Name': bill['Name'],
                'SummaryLaw': bill['SummaryLaw'],
                'LastUpdatedDate': bill['LastUpdatedDate'],
                'document': bill.get('document', ''),
                'present': bill.get('present', ''),
                'total_vote': bill['total_vote'],
                'in_favor': bill['in_favor'],
                'against': bill['against']
            }

            parties_data = {
                "BillID": bill['BillID'],
                "Likud_For": 0,
                "Likud_Against": 0,
                "YeshAtidNationalUnity_For": 0,
                "YeshAtidNationalUnity_Against": 0,
                "Shas_For": 0,
                "Shas_Against": 0,
                "Mafdal_ReligiousZionism_For": 0,
                "Mafdal_ReligiousZionism_Against": 0,
                "UnitedTorahJudaism_For": 0,
                "UnitedTorahJudaism_Against": 0,
                "OtzmaYehudit_For": 0,
                "OtzmaYehudit_Against": 0,
                "YisraelBeiteinu_For": 0,
                "YisraelBeiteinu_Against": 0,
                "UnitedArabList_For": 0,
                "UnitedArabList_Against": 0,
                "Hadash_Taal_For": 0,
                "Hadash_Taal_Against": 0,
                "LaborParty_For": 0,
                "LaborParty_Against": 0,
                "Noam_For": 0,
                "Noam_Against": 0
            }
            bills_collection.insert_one(bill_data)
            parties_collection.insert_one(parties_data)
        except Exception as e:
            error_response = {'error': str(e)}
            if str(e) == 'document':
                try:
                    bill_data = {
                        'BillID': bill['BillID'],
                        'Name': bill['Name'],
                        'SummaryLaw': bill['SummaryLaw'],
                        'LastUpdatedDate': bill['LastUpdatedDate'],
                        'present': bill.get('present', ''),
                        'total_vote': bill['total_vote'],
                        'in_favor': bill['in_favor'],
                        'against': bill['against']
                    }
                    bills_collection.insert_one(bill_data)
                except Exception as e:
                    error_response = {'error': str(e)}
                    print(error_response)
            print(error_response)

def update_every_24_hours():
    while True:
        update_new_bills()
        time.sleep(60 * 60 * 24)

update_thread = threading.Thread(target=update_every_24_hours)
update_thread.start()