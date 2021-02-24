import pymongo
from flask import Flask, jsonify, abort, make_response,request
from bson.json_util import dumps
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
# 跨域支持
CORS(app)

app.config["DEBUG"] = True

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["users"]
mycol = mydb["accounts"]
#def check_request_user(request_data):

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello Flask!</h1>"
#db = mongo.db.t1
@app.route('/users/<int:id>', methods=['GET'])
def getUsersData(id):
    
    result = mycol.find_one({'_id':id})

    return make_response(jsonify(result))

@app.route('/users', methods=['GET'])
def getAllUsersData():
    
    result = dumps(mycol.find())
    #result = '1236588'
    return make_response(jsonify(result))
    #return result

@app.route('/login', methods=['POST'])
def User_login():
    #將request資料轉換
    request_data = request.get_json()
    #return make_response(jsonify(request_data))
    #確認request的兩個key都有帶
    if 'account' in request_data:
        request_account = request_data.get('account')
    else:
        return jsonify("錯誤!沒有帳號欄位")

    if 'password' in request_data:
        request_password = request_data.get('password')
    else:
        return jsonify("錯誤!沒有密碼欄位")
    #將請求的帳號拿去資料庫查詢,並得到該筆資料
    result = mycol.find_one({'account':request_account})
    #若沒此帳號則回傳
    if(result == None):
        respone = make_response({'res_code': 402,'msg':'查無此帳號'})
        return respone
    #有帳號則比對密碼
    #將該帳號的密碼取出比對
    result_password = result.get('password')
    if(result_password == request_password):
        respone = make_response({'res_code': 200,'msg':'帳號密碼正確'})
        return respone
    else:
        respone = make_response({'res_code': 401,'msg':'密碼錯誤'})
        return respone


@app.route('/users', methods=['POST'])
def create_User():
    request_data = request.get_json()
    #確認request的兩個key都有帶
    if ('account' in request_data) and ('password' in request_data):
        #request_account = request_data.get('account')
        insert_data = {'account':request_data.get('account'),'password':request_data.get('password')}
    else:
        return jsonify("錯誤!沒有帳號密碼欄位")


    mycol.insert_one(insert_data)

    result = mycol.find_one({'account':request_data['account']})

    result.pop('_id')

    return jsonify(result)

@app.route('/users/<int:id>', methods=['PATCH'])
def update_users(id):
    request_data = request.json
    mycol.update_one({"_id":id}, { "$set": request_data })
    result = mycol.find_one({'_id':id})
    return jsonify(result)

@app.route('/users', methods=['DELETE'])
def delete_users():
    if 'username' in request.args:
        username = request.args['username']
    else:
        return jsonify("Error: No username provided. Please specify a username.")

    delete=mycol.delete_one({"username":username})
    results={'Deleted':delete.deleted_count}

    return jsonify(results)

if __name__ == '__main__':

    app.run(host='0.0.0.0')