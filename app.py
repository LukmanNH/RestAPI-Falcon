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
            if username == i['username'] and password == i['password']: 
                resp.body = json.dumps({
                    "code" : 200,
                    "messages" : "Berhasil Login",
                    "data" : {
                        "username" : data["username"],
                        "email" : i['email']
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
        email = data['email']

        for i in u.find():
            if username == i['username'] and email == i['email']:
                resp.body = json.dumps({
                    "code" : 409,
                    "massages" : "Gagal Register-- Username atau email telah digunakan "
                    })
                resp.status = falcon.HTTP_409
                return 
        u.insert({
            'email' : str(email),
            'username' : str(username),
            'password' : str(password)
        })
        resp.body = json.dumps({
                    "code" : 201,
                    "messages" : "Berhasil Register",
                    "data" : {
                        "username" : data["username"]
                    }
        })
        resp.status = falcon.HTTP_201

class ResetPassword():
    def on_post(self,req,resp):
        data  = json.loads(req.stream.read())

        username = data['username']
        email = data['email']
    
        reset_password = u.find_one_and_update({'username' : username,'email':email},{'$set':{'password':''}})
        if reset_password != None:
            resp.body = json.dumps({
                "code": 200,
                "message": 'Password berhasil di reset'
            })
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({
                "code" : 409,
                "message" : 'Akun tidak terdaftar'
            })
            resp.status = falcon.HTTP_404


class NewPassword():
    def on_post(self,req,resp):

        data = json.loads(req.stream.read())
        
        username = data['username']
        email = data['email']
        password = data['password']

        new_password = u.find_one_and_update({'username': username, 'email' : email}, {'$set':{'password' : password}})
        if new_password is True:
            resp.body = json.dumps({
                "code" : 409,
                "message" : 'gagal di perbarui'
            })
            resp.status = falcon.HTTP_404
            
        else:
            resp.body = json.dumps({
                "code": 200,
                "message": 'Password berhasil di perbarui'
            })
            resp.status = falcon.HTTP_200
            




        
                
            

api = falcon.API()
api.add_route('/login', Login())
api.add_route('/register', Register())
api.add_route('/reset', ResetPassword())
api.add_route('/new_pass' , NewPassword())


