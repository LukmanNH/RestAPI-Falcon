from pymongo import MongoClient
import pymongo
import json
import falcon

client = pymongo.MongoClient("mongodb+srv://luckman004:hackerisart1@cluster0-oacif.mongodb.net/login?retryWrites=true&w=majority")
db = client.login

u = db.user

class ObjRequestClass():
    def on_post(self , req, resp):
        data = json.loads(req.stream.read())

        username = data['username']
        password = data['password']
        for i in u.find():
            print(i)
            if username in i['username'] and password in i['password']:
                resp.body = json.dumps({
                    "code" : 200,
                    "messages" : "Berhasil Login",
                    "data" : {
                        "username" : data["username"],
                        "password" : ""
                    }
                })
                resp.status = falcon.HTTP_200
            else:   
                resp.body = json.dumps({
                    "code" : 401,
                    "massages" : "Gagal Login-- username atau password salah"
                })
                resp.status = falcon.HTTP_401



        

api = falcon.API()
api.add_route('/login', ObjRequestClass())

