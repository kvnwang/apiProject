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
    for user in users:
        print(user)
        res.append(convert_user(dict(user)))
    return res

def valid_params(filterData):
    s=set(('name', 'email', 'age', 'phone', 'address'))
    for v in filterData:
        if v not in s:
            return False
    return True

def normalize_params(data):
    if 'age' in data:
        data['age']=str(data['age'])
    if 'phone' in data:
        data['phone']=str(data['phone'])
    return data