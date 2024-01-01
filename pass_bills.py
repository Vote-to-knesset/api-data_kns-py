# from pymongo import MongoClient
# from set_tables import *
# from datetime import datetime
# from dotenv import load_dotenv
# import os
# import datetime
# load_dotenv()
#
#
#
#
# client = MongoClient(os.environ.get('SECRET_MONGO'))
# db = client['kns_data']
#
# import requests
#
# url = "https://www.knesset.gov.il/WebSiteApi/knessetapi/Votes/GetVoteDetails/39971"
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
#     print(response.json())
# else:
#     print(f"Request failed with status code: {response.status_code}")


from pymongo import MongoClient
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Connect to MongoDB
client = MongoClient(os.environ.get('SECRET_MONGO'))
db = client['kns_data']
collection = db['laws_collection']  # Replace 'laws_collection' with your collection name

# Function to fetch and update data for a specific law vote
def update_law_vote(vote_id):
    url = f"https://www.knesset.gov.il/WebSiteApi/knessetapi/Votes/GetVoteDetails/{vote_id}"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "if-none-match": "W/\"340ee0d3-ff84-43dd-a3e8-d01efc29903f\"",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://main.knesset.gov.il/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        law_data = response.json()
        new_laws_data = {
            'VoteId': law_data['VoteHeader'][0]['VoteId'],
            'VoteDate': law_data['VoteHeader'][0]['VoteDate'],
            'VoteType': law_data['VoteHeader'][0]['VoteType'],
            'ItemTitle': law_data['VoteHeader'][0]['ItemTitle'],
            'FK_ItemID': law_data['VoteHeader'][0]['FK_ItemID'],
            'Decision': law_data['VoteHeader'][0]['Decision'],
            'IsForAccepted': law_data['VoteHeader'][0]['IsForAccepted'],
            'AcceptedText': law_data['VoteHeader'][0]['AcceptedText'],
            'VoteCounters': law_data['VoteCounters'],
            'VoteDetails': law_data['VoteDetails']
        }

        collection.update_one(
            {"VoteId": law_data['VoteHeader'][0]['FK_ItemID']},
            {"$set": new_laws_data},
            upsert=True
        )
        return law_data.get('NextAndPrevVotes', {})
    else:
        print(f"Request for vote ID {vote_id} failed with status code: {response.status_code}")
        return {}

# Update data for the law vote with ID 39971 as an example
next_prev_votes = update_law_vote(40241)
print(next_prev_votes)
print(f"Updated law data for vote ID 39971")

# Example: Continuously update data for the next votes until there's no 'NextVote' available
while next_prev_votes and next_prev_votes[0]['NextVote']:
    next_vote_id = next_prev_votes[0]['NextVote']
    next_prev_votes = update_law_vote(next_vote_id)
    print(f"Updated law data for vote ID {next_vote_id}")

client.close()  # Close MongoDB connection
