from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
app = Flask(__name__)
import utils
import json
from bson import ObjectId


client =None
SECRET_KEY = os.environ.get('IS_DOCKER')
if(SECRET_KEY!=None):
    client = MongoClient('mongodb://mongodb:27017/')
else:
    client = MongoClient("localhost:27017")

# client = MongoClient('localhost:27017')

db = client.ContactDB
# test route
@app.route("/", methods = ['GET'])
def test():  return jsonify({"version":"1.0"})



# adds a user into db
@app.route("/api/add_user", methods = ['POST'])
def addUser():
    try:
        userData=dict(json.loads(str(request.data, encoding='utf-8')))
        if('name' not in userData or 'email' not in userData or 'age' not in userData or 'phone' not in userData or 'address' not in userData):
            return dumps({'error': "invalid"})
        status=db.Users.insert(userData)
        user=db.Users.find_one({"_id": ObjectId(status)})
        return jsonify(utils.convert_user(user))

    except Exception as e:
        return dumps({'error' : str(e)})


# gets all users from db
@app.route("/api/users", methods = ['GET'])
def allUsers():
    try:
        contacts = db.Users.find()
        return dumps(utils.convert_users(contacts))
    except Exception as e:
        return dumps({'error' : str(e)})


# gets a user with the given id
@app.route('/api/user/<string:user_id>',methods = ['GET'])
def user_details(user_id):
    try:
        user = db.Users.find_one({"_id": ObjectId(user_id)})
        return dumps(utils.convert_user(user))
    except Exception as e:
        return dumps({'error' : str(e)})


# deletes all Users
@app.route("/api/delete_users", methods = ['DELETE'])
def deletUsers():
    try:
        db.Users.delete_many({})
        return Response({"OK"}, status=200)
    except Exception as e:
        return dumps({'error' : str(e)})




# gets all users with filtered
@app.route("/api/get_user", methods = ['GET'])
def getUser():
    try:
        userData=None
        if(request.data==None or len(request.data)==0):
            userData={}
        else:
            userData=dict(json.loads(str(request.data, encoding='utf-8')))

        contacts = db.Users.find(utils.normalize_params(userData))
        return dumps(utils.convert_users(contacts))
    except Exception as e:
        return dumps({'error' : str(e)})


# deletes User with id
@app.route("/api/delete_user/<string:user_id>", methods = ['DELETE'])
def deleteOne(user_id):
    try:
        db.Users.delete_one({"_id": ObjectId(user_id)})
        return jsonify({"user": "OK"})
    except Exception as e:
        return dumps({'error' : str(e)})


# updates user
@app.route("/api/update_user/<string:user_id>", methods = ['PATCH'])
def update_user(user_id):
    try:
        filterData=dict(json.loads(str(request.data, encoding='utf-8')))
        if(utils.valid_params(filterData)==False):
            return dumps({'error': "invalid"})
        status = db.Users.update_one({"_id": ObjectId(user_id)}, {"$set": filterData})
        user = db.Users.find_one({"_id": ObjectId(user_id)})
        return jsonify(utils.convert_user(user))
    except Exception as e:
        return dumps({'error' : str(e)})






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
