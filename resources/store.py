import uuid
from flask import request
from flask.views import MethodView  # used for creating class and methods of class
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from db import db
from models import StoreModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


# A Blueprint in flask-smorest is used to divide an API into multiple segments
# This will go into API documentation

blp = Blueprint("stores", __name__, description="Store Operations")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        # raise NotImplementedError("Deleting a store is not implemented.")
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted!"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return {"stores": list(stores.values())}
        # return stores.values()
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # store_data = request.get_json()

        # if "name" not in store_data:
        #     abort(400, message="Bad Request, Ensure 'name' is present in JSON payload")
        
        # store_id = uuid.uuid4().hex
        # new_store = {**store_data, "id": store_id}
        # stores[store_id] = new_store
        # return new_store, 201
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")
        return store


        
