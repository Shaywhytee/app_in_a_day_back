from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Account_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, nullable=False, unique=True)
    user_password = db.Column(db.String, nullable=False)
    user_items = db.relationship('User_list_item', backref='account', lazy=True)

    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = user_password

class User_list_item(db.model):
    id = db.Column(db.Integer, praimary_key=True)
    type = db.Column(db.String, nullable=False)
    proof = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account_info.id'), nullable=False)

    def __init__(self, type, proof, account_id)
        self.type = type
        self.proof = proof
        self.account_id = account_id

class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_email', 'user_password', 'user_items')
account_schema = AccountSchema() 

class UserListItemSchema(ma.Schema):
    class Meta:
        field = ('id', 'user_email', 'user_password', 'user_items')
user_list_item_schema = UserListItemSchema()
user_list_item_schema = UserListItemSchema(many=True)

#***** Account Endpoints *****
    #Create

@app.route('/account/create', methods=["POST"])
def account_create():
    if request.content_type != 'application/json':
        return jsonify({"Error: JSONIFY"}), 400
    
    post_data = request.get_json()
    user_email = post_data.get('user_email')
    user_password = post_data.get('user_password')

    if user_email == None:
        return jsonify({"Error: Email is required"}), 400
    
    if user_password == None:
        return jsonify({"Error: Password is required"}), 400
    try:
        new_account = Account_info(user_email, user_password)
        db.session.add(new_account)
        db.session.commit()
        return jsonify({'success': 'Account created successfully'})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'Error': 'Email already exists.'}), 400
    except:
        db.session.rollback()
        return jsonify({'Error': 'Unable to create account'}), 500
    
    #Login
@app.route('/login', methods=["POST"])
def login():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid content type: must be 'application/json'"}), 400
    
    post_data = request.get_json()
    email = post_data.get("user_email")
    password = post_data.get("user_password")

    if not email or not password:
        return jsonify({"error": "Invalid email or password"}), 401

    account = db.session.query(Account_info).filter(Account_info.user_email == email, Account_info.user_password == password).first()

    if account is None:
        return jsonify({'error': 'Invalid email or password'}), 401
    else:
        return jsonify({"success": "Account log in successful"}, account_schema.dump(account.id))


if __name__ == '__main__':
    app.run(debug=True)


#***** User item endpoints *****
    #create
@app.route('/create/item', methods=["POST"])
def createItem():
    if request.content_type != 'application/json':
        return jsonify({"error": "Invalid content type: must be 'application/json'"}), 400
    
    post_data=
    #delete
    #edit