from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required
import sys
import traceback
from sqlalchemy.orm.exc import NoResultFound

bp = Blueprint('api', __name__, url_prefix='/api')

# user route
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

# logout route
@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

# login route
@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    user = None  # Initialize user variable
    try:
        user = db.query(User).filter(User.email == data['email']).one()
        if user.verify_password(data['password']) == False:
                return jsonify(message = 'Incorrect credentials'), 400
        session.clear()
        session['user_id'] = user.id
        session['loggedIn'] = True
        return jsonify(id = user.id)
    except NoResultFound:
        return jsonify(message='Incorrect credentials'), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify(message='An error occurred'), 500    


# comment route
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    data = request.get_json()
    db = get_db()

    try:
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )
        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify(message = 'Comment failed'), 500
    return jsonify(id = newComment.id)


# upvote route
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()

    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed'), 500
    return '', 204

# create a post
@bp.route('/posts', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()

    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500
    return jsonify(id = newPost.id)


# updating a single post
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
    data = request.get_json()
    db = get_db()

    try:
        # retrieve post and update title property
        post = db.query(Post).filter(Post.id == id).one()
        post.title = data['title']
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404
    return ''; 204


# delete a post
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()

    try:
        # delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404
    return '', 204
