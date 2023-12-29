# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# import pymongo
#
# app = Flask(__name__)
# CORS(app)
#
# # Configure JWT
# app.config['JWT_SECRET_KEY'] = 'your-secret-key'
# jwt = JWTManager(app)
#
# # Connect to MongoDB
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['the_database']
# users_collection = db['users']
#
# # Bcrypt for password hashing
# bcrypt = Bcrypt(app)
#
# @app.route('/userProfile', methods=['POST'])
# @jwt_required()
# def user_profile():
#     # Fetch user profile information using the current user's identity
#     current_user_email = get_jwt_identity()
#
#     user_data = users_collection.find_one({'email': current_user_email}, {'_id': 0, 'password': 0})
#
#     if user_data:
#         return jsonify(user_data)
#     else:
#         return jsonify({'message': 'User not found'}), 404
#
# @app.route('/signup', methods=['POST'])
# def register():
#     data = request.get_json()
#
#     # Hash the password before storing in MongoDB
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
#
#     # Store user information in MongoDB with hashed password
#     users_collection.insert_one({
#         'firstName': data['firstName'],
#         'lastName': data['lastName'],
#         'email': data['email'],
#         'password': hashed_password,
#     })
#
#     return jsonify({'message': 'Registration successful'}), 201
#
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = users_collection.find_one({'email': data['email']})
#
#     if user and bcrypt.check_password_hash(user['password'], data['password']):
#         # Generate access token and return it
#         access_token = create_access_token(identity=data['email'])
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({'message': 'Invalid credentials'}), 401
#
# def home():
#     return 'Welcome to the backend of your website!'
#
# if __name__ == '_main_':
#     app.run(debug=True)
