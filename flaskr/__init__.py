from flask import Flask, jsonify, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from models import Account, setup_db, db
from flask_cors import CORS
import sys


def create_app(test_config=None):
    app = Flask(__name__)

    # Connecting to SQLAlchemy database
    setup_db(app)
    
    # Defining CORS headers
    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE')
        return response

    @app.route('/')
    def index():
        number_of_accounts = len(Account.query.all())
        return render_template('index.html', accounts=number_of_accounts), 200


    @app.route('/accounts/create', methods=['POST'])
    def create_account():
        error = False
        req_body = request.get_json()
        res_body = {}

        # Aborting if the user didn't submit a field
        for info, value in req_body.items():
            if len(value) == 0:
                error = True
                abort(400)

        # Assigning information from the JSON request to variables
        first_name = req_body['first_name']
        last_name = req_body['last_name']
        balance = int(req_body['balance'])
        password = req_body['password']


        try:
            new_account = Account(first_name=first_name, last_name=last_name,
                                    password=password, balance=balance)
            db.session.add(new_account)
            db.session.commit()
            res_body['id'] = new_account.id
            res_body['first_name'] = new_account.first_name
            res_body['last_name'] = new_account.last_name
            res_body['balance'] = new_account.balance
            res_body['success'] = True
            
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            number_of_accounts = len(Account.query.all())
            res_body['new_number_of_accounts'] = number_of_accounts
            db.session.close()

        if error:
            abort (422)
        else:
            return jsonify(res_body)

    @app.route('/accounts/<int:id>/<pw>')
    def show_account(id, pw):
        error = False
        account = Account.query.get(id)

        if not account:
            abort (404)
        elif pw != account.password:
            abort(401)
        else:
            res_body = {}
            res_body['id'] = account.id
            res_body['first_name'] = account.first_name
            res_body['last_name'] = account.last_name
            res_body['balance'] = account.balance
            res_body['success'] = True       

            return jsonify(res_body)

    @app.route('/accounts/<int:id>/withdraw', methods=['PATCH'])
    def deposite(id):
        error = False
        account = Account.query.get(id)
        req_body = request.get_json()
        res_body = {}

        withdrawn_amount = req_body['action_amount']
        if not withdrawn_amount:
            abort (400)
        elif int(withdrawn_amount) > account.balance:
            abort (422)
        else:
            try:
                account.balance -= int(withdrawn_amount)
                res_body['new_amount'] = account.balance
                res_body['success'] = True
                db.session.commit()
            except:
                error = True
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            
            if error:
                abort (422)
            else:
                return jsonify(res_body)

    @app.route('/accounts/<int:id>/deposit', methods=['PATCH'])
    def deposit(id):
        error = False
        account = Account.query.get(id)
        req_body = request.get_json()
        res_body = {}

        deposit_amount = req_body['action_amount']

        if not deposit_amount:
            abort (400)
        
        try:
            account.balance += int(deposit_amount)
            res_body['new_amount'] = account.balance
            res_body['success'] = True
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort (422)
        else:
            return jsonify(res_body)

    @app.route('/accounts/<int:id>/delete', methods=['DELETE'])
    def delete_account(id):
        error = False
        account = Account.query.get(id)
        res_body = {}
        try:
            res_body['success'] = True
            res_body['first_name'] = account.first_name
            res_body['last_name'] = account.last_name
            res_body['remaining_balance'] = account.balance
            Account.query.filter_by(id=id).delete()
            res_body['remaining_accounts'] = len(Account.query.all())
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        
        if error:
            abort (422)
        else:
            return jsonify(res_body)

    @app.route('/accounts/<int:id>/modify_name', methods=['PATCH'])
    def modify_name(id):
        error = False
        account = Account.query.get(id)
        req_body = request.get_json()
        res_body = {}

        if req_body['first_name'] == '' or req_body['last_name'] == '':
            abort (400)
        
        try:
            account.first_name = req_body['first_name']
            account.last_name = req_body['last_name']
        
            res_body['success'] = True
            res_body['first_name'] = account.first_name
            res_body['last_name'] = account.last_name
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        
        if error:
            abort (422)

        return jsonify(res_body)

    @app.route('/accounts/<int:id>/modify_password', methods=['PATCH'])
    def modify_password(id):
        error = False
        account = Account.query.get(id)
        req_body = request.get_json()
        res_body = {}

        if req_body['old_password'] == '' or req_body['new_password'] == '':
            abort (400)
        if req_body['old_password'] != account.password:
            abort (401)
        
        try:
            account.password = req_body['new_password']
            res_body['success'] = True
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        
        if error:
            abort (422)

        return jsonify(res_body)


# Error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'There is a missing field'
        }), 400
    
    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Sorry, that password is not correct!'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'The request could not be completed'
        }), 422


    return app