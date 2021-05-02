from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):

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


class Items(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run()
