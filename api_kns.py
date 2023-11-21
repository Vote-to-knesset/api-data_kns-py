from flask import Flask, request, jsonify, abort
from config import *
from KNS_data import *
import db_kns
import json
from pymongo import MongoClient
from flask_cors import CORS

import os
SECRET_MONGO = os.getenv('SECRET_MONGO')


SECRET_API_KEY = os.getenv('SECRET_API_KEY')
app = Flask(__name__)
CORS(app)


def authenticate_request():
    api_key = request.headers.get('Authorization')

    if api_key != SECRET_API_KEY:
        abort(401)

def update_bill_vote(data):
    client = MongoClient(SECRET_MONGO)  # Replace with your MongoDB connection URL
    db = client['kns_data']  # Replace with your MongoDB database name

    # Access your collections
    bills_collection = db['bills']
    bill_id_to_update = data['BillID']
    choice = data['choice']
    filter_criteria = {'BillID': bill_id_to_update}

    update_operation = {
        '$inc': {
            'total_vote': 1,
            choice: 1
        }
    }

    # Update the document with the specified BillID
    result = bills_collection.update_one(filter_criteria, update_operation)
    if result.matched_count > 0:
        print(f"Updated total_vote and in_favor for document with BillID: {bill_id_to_update}")
    else:
        print(f"No documents matched the filter criteria for BillID: {bill_id_to_update}")

    client.close()


def update_parties_vote(data):
    client = MongoClient(SECRET_MONGO)
    db = client['kns_data']

    bills_collection = db['parties']
    bill_id_to_update = data['BillID']
    party_to_update = data['party']
    filter_criteria = {'BillID': bill_id_to_update}
    update_operation = {
        '$inc': {
            party_to_update: 1,
        }
    }

    result = bills_collection.update_one(filter_criteria, update_operation)
    if result.matched_count > 0:
        print(f"Updated total_vote and in_favor for document with BillID: {bill_id_to_update}")
    else:
        print(f"No documents matched the filter criteria for BillID: {bill_id_to_update}")
    client.close()


def sort_bills_by_interest(data):
    sorted_data = sorted(data, key=lambda x: x['total_vote'], reverse=True)
    return sorted_data


@app.route('/', methods=['GET'])
def all():
    return "hi"



@app.route('/api/update_data', methods=['POST'])
def update_data():
    try:
        authenticate_request()
        data = request.get_json()

        update_bill_vote(data)
        update_parties_vote(data)

        response = {'message': 'Data updated successfully'}
        return jsonify(response), 200

    except Exception as e:
        error_response = {'error': str(e)}
        return jsonify(error_response), 500

def get_data_bills_from_db():
    try:
        client = MongoClient(SECRET_MONGO)
        db = client['kns_data']
        bills_collection = db['bills']

        sorted_bills = bills_collection.find({}, {'_id': 0})




        last_100_bills = list(sorted_bills)


        client.close()
        return last_100_bills
    except Exception as e:
        error_response = {'error': str(e)}

def get_data_parties_from_db():
    try:
        client = MongoClient(SECRET_MONGO)  # Replace with your MongoDB connection URL
        db = client['kns_data']  # Replace with your MongoDB database name
        parties_collection = db['parties']
        all_parties_data = list(parties_collection.find({}, {'_id': 0}))
        client.close()
        return all_parties_data
    except Exception as e:
        error_response = {'error': str(e)}



@app.route('/api/data_bills', methods=['GET'])
def api_data():
    data = get_data_bills_from_db()
    sorted_data = sort_bills_by_interest(data)
    response = json.dumps(sorted_data, ensure_ascii=False).encode('utf8')
    return response


def get_data_bills_comments_from_db(bill_id):
    try:
        client = MongoClient(SECRET_MONGO)
        db = client['kns_data']
        comments_collection = db['billsComment']
        all_comments_data = list(comments_collection.find({'billId': bill_id}, {'_id': 0}))
        client.close()
        return all_comments_data
    except Exception as e:
        error_response = {'error': str(e)}


@app.route('/api/get_comments', methods=['GET'])
def api_data_comments():
    bill_id = request.args.get('billId')
    print(bill_id)
    data = get_data_bills_comments_from_db(bill_id)
    response =json.dumps(data, ensure_ascii=False).encode('utf8')
    return response

@app.route('/api/data_parties', methods=['GET'])
def api_data_parties():
    data = get_data_parties_from_db()
    response = json.dumps(data, ensure_ascii=False).encode('utf8')
    return response


if __name__ == "__main__":
    app.run()

