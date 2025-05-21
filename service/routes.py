"""
Account Service Routes
"""

from flask import jsonify, request, abort, make_response, url_for
from service import app, db
from service.models import Account
from service.common import status  # HTTP Status Codes


@app.route("/")
def index():
    return "Welcome to the Account RESTful Service!", status.HTTP_200_OK


@app.route("/health")
def health():
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_account():
    if not request.is_json:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")

    data = request.get_json()
    try:
        account = Account()
        account.deserialize(data)
        db.session.add(account)
        db.session.commit()
    except KeyError as error:
        abort(status.HTTP_400_BAD_REQUEST, f"Missing field: {error.args[0]}")

    location_url = url_for("get_account", account_id=account.id, _external=True)
    return make_response(jsonify(account.serialize()), status.HTTP_201_CREATED, {"Location": location_url})


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' not found.")
    return jsonify(account.serialize()), status.HTTP_200_OK
