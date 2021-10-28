from dataclasses import asdict

from flask import jsonify, request
from flask.views import MethodView
from flask_contacts_demo.data_layer import DB, PhoneBookEntry

import humps


def serialize(e: PhoneBookEntry):
    return jsonify(humps.camelize(asdict(e)))


def serialize_many(entries: list[PhoneBookEntry]):
    return jsonify(humps.camelize([asdict(e) for e in entries]))


def deserialize(e: dict):
    return humps.decamelize(e)


class PhoneBookAPI(MethodView):
    def __init__(self, db: DB) -> None:
        super().__init__()
        self.db = db

    def get(self):
        entries = self.db.get_entries()
        return serialize_many(entries)

    def post(self):
        body = request.get_json()
        print(body)
        new_entry = self.db.add_entry(**deserialize(body))
        return serialize(new_entry)

    def delete(self, id):
        delete_count = self.db.delete_entry(id)
        if delete_count > 0:
            return ('', 200)
        else:
            return ('No such entry', 404)
        pass

    def put(self, id):
        body = request.get_json()
        new_entry = self.db.update_entry(
            **deserialize(body)
        )
        return serialize(new_entry)
