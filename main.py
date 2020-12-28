from flask_restful import Api, Resource
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

# hello is my collection name
app = Flask(__name__)
api = Api(app)

# define path for our mongodb database
app.config["MONGO_URI"] = "mongodb://mongo:27017/maulik"
#initialize pymongo with mongo object
mongo = PyMongo(app)
class Register(Resource):
   def post(self):
        username = request.json['name']
        email = request.json['email']
        pswd = request.json['pswd']
        #check user already exist by username
        if mongo.db.hello.find_one({'name': username}) is None:
            x = mongo.db.hello.insert({'name': username, 'email': email, 'pswd': pswd})
            return jsonify("registered successfully!")
        else:
            return jsonify("user already registered!")


class Login(Resource):
    def post(self):
        username = request.json['name']
        pswd = request.json['pswd']
        x = mongo.db.hello.find_one({'name': username})

        if pswd == x['pswd']:
            return jsonify("login done!")

        else:
            return jsonify("invalid entry")


class changepass(Resource):
    def post(self):

        username = request.json['name']
        old_pass = request.json['old_pass']
        new_pass = request.json['new_pass']
        x = mongo.db.hello.find_one({'name': username})
        if old_pass == x['pswd']:
            mongo.db.hello.update_one({'name': username}, {"$set": {'pswd': new_pass}})
            return jsonify("password changed !")
        else:
            return jsonify("invaid username and password!")


class forgot_pass(Resource):
    def post(self):
        username = request.json['name']
        email = request.json['email']
        new_pass = request.json['new_pass']
        y = mongo.db.hello.find_one({'name': username})
        if username == y['name']:
            if email == y['email']:
                mongo.db.hello.update_one({'name': username}, {"$set": {'pswd': new_pass}})
                return jsonify("password  reset successful!")
            else:
                return jsonify("email does not exist!")
        else:
            return jsonify("username does not exist!")


class get_allusers(Resource):
    def get(self):
        y = list(mongo.db.hello.find({}, {"_id": 0}))
        return y


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(changepass, '/changepass')
api.add_resource(forgot_pass, '/forgot_pass')
api.add_resource(get_allusers, '/get_allusers')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
