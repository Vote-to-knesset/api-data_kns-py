from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
import datetime
load_dotenv()




# Assuming SECRET_MONGO is your MongoDB connection string
client = MongoClient(os.environ.get('SECRET_MONGO'))
db = client['kns_data']
bills_collection = db['bills']
comments_collection = db['billsComment']

# Find all documents in the bills collection
sorted_bills = bills_collection.find({}, {'_id': 0})


# Iterate through each bill document
for bill in sorted_bills:
    # Extract the billid from the document
    billid = bill.get('BillID')

    # Create a new comment
    comment = {
        "text": "This is the first comment.",
        "author": "User1",
        "timestamp": datetime.utcnow().isoformat()  # You can modify this based on your timestamp logic
    }

    # Create a document for the bill in the comments collection if it doesn't exist
    comments_collection.update_one({'billid': billid}, {'$setOnInsert': {'billid': billid}}, upsert=True)

    # Update the document in the comments collection by adding the comment to the list of comments
    comments_collection.update_one({'billid': billid}, {'$push': {'comments': comment}})
