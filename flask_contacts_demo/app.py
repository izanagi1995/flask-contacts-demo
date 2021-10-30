import atexit

from flask.app import Flask
from flask_contacts_demo.data_layer import DB
from flask_contacts_demo.views import PhoneBookAPI


app = Flask(__name__)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response


db = DB()
view = PhoneBookAPI.as_view("phone_book_api", db)
app.add_url_rule(
    "/api/entries/", view_func=view, methods=["GET", ]
)
app.add_url_rule(
    "/api/entries/", view_func=view, methods=["POST", ],
)
app.add_url_rule(
    "/api/entries/<int:id>", view_func=view, methods=["PUT", "DELETE"]
)


def on_exit():
    db.commit_and_close()


atexit.register(on_exit)


if __name__ == '__main__':
    app.run()