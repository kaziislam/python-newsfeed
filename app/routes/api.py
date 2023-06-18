from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    #print(data)
    db = get_db()

    try: 
        # attempt creating a new user
        # create a new user
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save in database
        db.add(newUser)
        db.commit()
    except: 
        print(sys.exc_info()[0])
        # insert failed, so send error to frontend
        db.rollback()
        return jsonify(message = 'Signup failed'), 500
    
    # user's session information 
    # This clears any existing session data and creates two new session properties
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True
    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])
        return jsonify(message = 'Incorrect credentials'), 400
    
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True
    return jsonify(id = user.id)