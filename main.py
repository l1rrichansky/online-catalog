from app import app
from app import db
import view
from flask import session
from items.blueprint import items

app.register_blueprint(items, url_prefix='/catalog')


if __name__ == "__main__":
    app.run(debug=True)



