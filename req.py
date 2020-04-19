import json

from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app, "/v0.1")


with open('data.json') as data:
    data = json.load(data)


class User(Resource):
    def get(self, name):
        for user in data:
            if(name == user["name"]):
                return make_response(jsonify({'data': user}), 200)
        return make_response(jsonify({'message': "User not found"}), 404)

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for k, user in data:
            if(name == user["name"]):
                user["age"] = int(args["age"])
                user["occupation"] = args["occupation"]
                data[k] = user
                with open('data.json', 'w+') as fileData:
                    json.dump(data, fileData)
                return make_response(jsonify({"data": data}), 201)

    def delete(self, name):
        global data
        ndata = [user for user in data if user["name"] != name]
        data = ndata
        with open('data.json', 'w+') as fileData:
            json.dump(data, fileData)
        return make_response(jsonify({'message': "{} is deleted.".format(name)}), 200)


class Users(Resource):
    def get(self):
        return make_response(jsonify({'data': data}), 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in data:
            if(args["name"] == user["name"]):
                return make_response(jsonify({'message': "User with name {} already exists".format(args["name"])}), 400)

        user = {
            "name": args["name"],
            "age": int(args["age"]),
            "occupation": args["occupation"]
        }

        data.append(user)

        with open('data.json', 'w+') as fileData:
            json.dump(data, fileData)
        return make_response(jsonify({'data': data}), 201)


# api.add_resource(Users, "/users")
api.add_resource(User, '/users/<string:name>', endpoint="user")
api.add_resource(Users, '/users', endpoint="users")
app.run(debug=True)
