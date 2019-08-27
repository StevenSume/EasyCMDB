from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from . import create_app, db
from .error import InvalidUsage
from .models import Project, Item
from flask import request
import json
from collections import Iterable

app = create_app()
auth = HTTPBasicAuth()

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/token')
@auth.login_required
def get_auth_token():
    s = Serializer(app.config['SECRET_KEY'],expires_in=app.config['TOKEN_EXPIRES_IN'])
    token = s.dumps({'SECRET_KEY': app.config['SECRET_KEY']})
    return jsonify({ 'token': token.decode('ascii') })

@auth.verify_password
def verify_password(username_or_token, password):
    if verify_auth_token(username_or_token) is True:
        return True
    elif username_or_token == app.config['USERNAME'] and password == app.config['PASSWORD']:
        return True
    else:
        return False

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return app.config['SECRET_KEY'] == data['SECRET_KEY']

def get_return_data(query_results):
    data = []
    if isinstance(query_results, Iterable):
        for i in query_results:
            data.append(i.to_dict())
        return jsonify(data)
    else:
        return jsonify(query_results.to_dict())

@app.route('/get/project',methods=['POST'])
@auth.login_required
def get_project_list():
    return get_return_data(Project.query.all())

@app.route('/get/items',methods=['POST'])
@auth.login_required
def get_items():
    data = json.loads(request.get_data().decode("utf-8"))
    project_name = data.get("project_name")
    project = Project.query.filter_by(project_name=project_name).first()
    return get_return_data(Item.query.filter_by(project_id=project.id).all())

@app.route('/create/project',methods=['POST'])
@auth.login_required
def create_project():
    data = json.loads(request.get_data().decode("utf-8"))
    project_name = data.get("project_name")
    project = Project(project_name=project_name)
    db.session.add(project)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    p = Project.query.filter_by(project_name=project_name).first()
    return get_return_data(p)

@app.route('/create/item',methods=['POST'])
@auth.login_required
def create_item():
    data = json.loads(request.get_data().decode("utf-8"))
    project_name = data.get("project_name")
    project = Project.query.filter_by(project_name=project_name).first()
    if project is None:
        return jsonify({ "status": "project is not exist" })
    key = data.get("key")
    item = Item.query.filter_by(project_id=project.id,key=key).first()
    value = data.get("value")
    if item is None:
        item = Item(project_id=project.id,key=key,value=value)
    else:
        item.value = value
    db.session.add(item)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return get_return_data(Item.query.filter_by(project_id=project.id).all())

@app.route('/delete/item',methods=['POST'])
@auth.login_required
def delete_item():
    data = json.loads(request.get_data().decode("utf-8"))
    project_name = data.get("project_name")
    project = Project.query.filter_by(project_name=project_name).first()
    key = data.get("key")
    item = Item.query.filter_by(project_id=project.id,key=key).first()
    db.session.delete(item)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return jsonify({ "status": "ok" })

@app.route('/delete/project',methods=['POST'])
@auth.login_required
def delete_project():
    data = json.loads(request.get_data().decode("utf-8"))
    project_name = data.get("project_name")
    project = Project.query.filter_by(project_name=project_name).first()
    items = Item.query.filter_by(project_id=project.id).all()
    for item in items:
        db.session.delete(item)
    db.session.delete(project)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return jsonify({"status": "ok"})

@app.route('/rename/project',methods=['POST'])
@auth.login_required
def rename_project():
    data = json.loads(request.get_data().decode("utf-8"))
    project_old_name = data.get("project_old_name")
    project = Project.query.filter_by(project_name=project_old_name).first()
    project_new_name = data.get("project_new_name")
    project.project_name=project_new_name
    db.session.add(project)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return get_return_data(Project.query.filter_by(project_name=project_new_name).first())



