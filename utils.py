from flask import make_response

JSON_MIME_TYPE = 'application/json'


def convert_user(user):
    return {
        "_id": str(user['_id']),
        "name": user['name'],
        "email": user['email'],
        "age": user['age'],
        "phone": user['phone'],
        "address": user['address']
    }

def convert_users(users):
    res=[]
    for user in users: res.append(convert_user(dict(user)))
    return res

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)

def valid_params(filterData):
    s=set(('name', 'email', 'age', 'phone', 'address'))
    for v in filterData:
        if v not in s:
            return False
    return True

