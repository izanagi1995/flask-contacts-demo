from flask_contacts_demo.data_layer import DB
from tempfile import TemporaryDirectory
from os import path


def test_db():
    with TemporaryDirectory() as d:
        db = DB(path.join(d, "db.sqlite3"))
        assert len(db.get_entries()) == 0
        nico = db.add_entry("0123456789", "Nicolas")
        assert nico.id != 0
        assert len(db.get_entries()) == 1
        assert db.delete_entry(nico.id) != 0
        assert len(db.get_entries()) == 0
