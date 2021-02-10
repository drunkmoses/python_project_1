from flask import Flask, request
import db_connector
import pymysql

app = Flask(__name__)

# local users storage
users = {}
# supported methods
@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):

    if request.method == 'POST':
        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        users[user_id] = user_name
        try:
            db_connector.insert_db(user_id,user_name) #
            print("User added successfully")
            return {'status': 'ok', 'user_added': user_name}, 200 # status code
        except pymysql.err.IntegrityError:
            print("User already exists")
            return {'status': 'error', 'reason': 'id already exists'}, 500 # error status code

    elif request.method == 'GET':
        try:
            user_name = db_connector.select_db(user_id)
            return {'status': 'ok', 'user_name': user_name}, 200 # status code
        except:
            return {'status': 'error', 'reason': 'id not found'}, 500 # error status code

    elif request.method == 'PUT':
        request_data = request.json
        user_name = request_data.get('user_name')
        users[user_id] = user_name
        try:
            db_connector.update_db(user_id, user_name)
            return {'user_id': user_id, 'user_updated': users[user_id]}, 200 # status code
        except:
            return {'status': 'error', 'reason': 'no such id'}, 500 # error status code

    elif request.method == 'DELETE':
        try:
            db_connector.delete_db(user_id)
            return {'user_id': user_id, 'user_deleted': user_id}, 200 # status code
        except:
            return {'status': 'error', 'reason': 'no such id'}, 500 # error status code


# host is pointing at local machine address
# debug is used for more detailed logs + hot swaping
# the desired port - feel free to change
app.run(host='127.0.0.1', debug=True, port=5000)