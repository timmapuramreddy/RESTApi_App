from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This filed cannot be left blank!")
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a store id!")

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found!!'}, 400

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with the name {0} already exists in server.'.format(name)}, 400

        #data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel(name, **data) # item = ItemModel(name, data['price'], data['store_id'])

        try:
            # ItemModel.insert_item(item)
            item.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'An error occured inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item successfully deleted'}
        return {'message': 'Item not found!!'}, 400


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data) # data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
