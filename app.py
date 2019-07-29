import pymongo
import json
import falcon
from falcon.http_status import HTTPStatus
from falcon_cors import CORS
import jwt

client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0-oacif.mongodb.net/login?retryWrites=true&w=majority")
db = client.login

cors = CORS(allow_origins_list=['http://localhost:3000/'])

u = db.user

class Login(object):
    @classmethod
    def on_post(self , req, resp):
        data = json.loads(req.bounded_stream.read().decode('UTF-8'))
        # data = json.loads(req.bounded_stream.read())

        username = data['username']
        password = data['password']
        for i in u.find():
            if username == i['username'] and password == i['password']:
                resp.body = json.dumps({
                    "code" : 200,
                    "messages" : "Login Success",
                    "data" : {
                        "username" : data["username"],
                        "email" : i['email']
                    }
                })
                resp.status = falcon.HTTP_200
                return
            else:
                resp.body = json.dumps({
                    "code" : 401,
                    "massages" : "Gagal Login-- username atau password salah"
                })
                resp.status = falcon.HTTP_401

class Register():
    @classmethod
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
    @classmethod
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
                "message" : 'Gagal reset password --Sorry'
            })
            resp.status = falcon.HTTP_404


class NewPassword():
    @classmethod
    def on_post(self,req,resp):
        data = json.loads(req.stream.read())

        username = data['username']
        email = data['email']
        password = data['password']

        new_password = u.find_one_and_update({'username': username, 'email' : email}, {'$set':{'password' : password}})
        if new_password is True:
            resp.body = json.dumps({
                "code" : 409,
                "message" : 'Gagal di perbarui'
            })
            resp.status = falcon.HTTP_404
        else:
            resp.body = json.dumps({
                "code": 200,
                "message": 'Password berhasil di perbarui'
            })
            resp.status = falcon.HTTP_200

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

api = falcon.API(middleware=[HandleCORS() ])
api.add_route('/login', Login())
api.add_route('/register', Register())
api.add_route('/reset', ResetPassword())
api.add_route('/new_pass' , NewPassword())
