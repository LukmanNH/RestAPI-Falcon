from pymongo import MongoClient
import pymongo
import json
import falcon

client = pymongo.MongoClient("mongodb+srv://luckman004:hackerisart1@cluster0-oacif.mongodb.net/test?retryWrites=true&w=majority")
db = client.login

u = db.user

class ObjRequestClass():
    def on_post(self , req, resp):
        data = json.loads(req.stream.read())

        for i in u.find():
            if data['username'] == i['username'] and data['password'] == i['password']:
                resp.body = json.dumps({
                    "code" : 200,
                    "messages" : "Berhasil Login",
                    "data" : {
                        "username" : data["username"]
                    }
                })
                print("Success")
                resp.status = falcon.HTTP_200
            else:   
                resp.body = json.dumps({
                    "code" : 401,
                    "massages" : "Gagal Login-- username atau password salah"
                })
                resp.status = falcon.HTTP_401
                print("Failed")

    # def on_post(self, req, resp):
    #     posted_data = json.loads(req.stream.read())
    #     print(str(type(posted_data)))
    #     print(posted_data)


        

api = falcon.API()
api.add_route('/login', ObjRequestClass())

