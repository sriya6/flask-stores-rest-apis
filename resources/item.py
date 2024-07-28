from flask import request
from flask.views import MethodView  # used for creating class and methods of class
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from schemas import ItemSchema, ItemUpdateSchema

from db import db
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("items", __name__, description="Item Operations")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found")
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted"}
        # except KeyError:
        #     abort(404, message="Oops, Item not found")
        item = ItemModel.query.get_or_404(item_id)
        # raise NotImplementedError("Deleting an item is not implemented.")
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted!"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.json()
        # try:
        #     item = items[item_id]
        #     item |= item_data  # Updating dict inplace using Augmented assignment union operator

        #     return item
        # except:
        #     abort(404, message="Item not found")
        item = ItemModel.query.get(item_id)
        # raise NotImplementedError("Updating an item is not implemented.")
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/item")
class ItemsList(MethodView):
    @jwt_required(fresh=True)
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # return {"items": list(items.values())}
        # return items.values()
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json()
        # item_id = uuid.uuid4().hex
        # new_item = {**item_data, "id": item_id}
        # items[item_id] = new_item
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting an item")

        return item
