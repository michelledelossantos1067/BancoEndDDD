from flask import Blueprint, request, jsonify
from app.database.config import SessionLocal
from app.services.account_service import AccountService

account_bp = Blueprint('accounts', __name__)

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    db = SessionLocal()
    try:
        data = request.get_json()
        
        if not data.get('holder_name') or not data.get('holder_id') or not data.get('account_type'):
            return jsonify({"error": "Missing required fields"}), 400
        
        account = AccountService.create_account(
            db,
            holder_name=data['holder_name'],
            holder_id=data['holder_id'],
            account_type=data['account_type']
        )
        
        return jsonify(account.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@account_bp.route('/accounts', methods=['GET'])
def get_all_accounts():
    db = SessionLocal()
    try:
        accounts = AccountService.get_all_accounts(db)
        return jsonify([account.to_dict() for account in accounts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@account_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    db = SessionLocal()
    try:
        account = AccountService.get_account_by_id(db, account_id)
        if not account:
            return jsonify({"error": "Account not found"}), 404
        return jsonify(account.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@account_bp.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    db = SessionLocal()
    try:
        data = request.get_json()
        account = AccountService.update_account(
            db,
            account_id=account_id,
            holder_name=data.get('holder_name'),
            account_type=data.get('account_type')
        )
        
        if not account:
            return jsonify({"error": "Account not found"}), 404
        
        return jsonify(account.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@account_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    db = SessionLocal()
    try:
        success = AccountService.delete_account(db, account_id)
        if not success:
            return jsonify({"error": "Account not found"}), 404
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()