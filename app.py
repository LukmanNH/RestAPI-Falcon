from pymongo import MongoClient
import pymongo
import json
import falcon
# from .models import User

client = pymongo.MongoClient("mongodb+srv://luckman004:hackerisart1@cluster0-oacif.mongodb.net/login?retryWrites=true&w=majority")
db = client.login

u = db.user

class Login(object):
    def on_post(self , req, resp):
        data = json.loads(req.stream.read())

        username = data['username']
        password = data['password']
        for i in u.find():
            if username in i['username'] and password in i['password']:
                resp.body = json.dumps({
                    "code" : 200,
                    "messages" : "Berhasil Login",
                    "data" : {
                        "username" : data["username"]
                    }
                })
                resp.status = falcon.HTTP_200
            else:   
                resp.body = json.dumps({
                    "code" : 401,
                    "massages" : "Gagal Login-- username atau password salah"
                })
                resp.status = falcon.HTTP_401

class Register():
    def on_post(self,req,resp):
        data  = json.loads(req.stream.read())

        username = data['username']
        password = data['password']

        for i in u.find():
            if username == i['username']:
                resp.body = json.dumps({
                    "code" : 409,
                    "massages" : "Gagal Register-- Username telah digunakan "
                    })
                resp.status = falcon.HTTP_409
                return 
                
        u.insert({
            'username' : str(username),
            'password' : str(password),
        })
        resp.body = json.dumps({
                    "code" : 201,
                    "messages" : "Berhasil Register",
                    "data" : {
                        "username" : data["username"]
                    }
        })
        resp.status = falcon.HTTP_201
        return 

        
                
            

api = falcon.API()
api.add_route('/login', Login())
api.add_route('/register', Register())


