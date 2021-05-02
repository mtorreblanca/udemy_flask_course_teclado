from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authentication, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authentication, identity )

items = []


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name , items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):

        if next(filter(lambda x: x['name'] == name , items), None):
            return {"message": "Item with name '{}' has already been created ".format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data["price"]}
        items.append(item)
        return {'item': item}, 201

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name , items), None)
        if item is None:
            item = {'name': name, 'price': data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "Item '{}' deleted".format(name)}


class Items(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run()
