from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database.config import SessionLocal
from app.services.transaction_service import TransactionService

transaction_bp = Blueprint('transaction', __name__)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        
        if not data or 'account_id' not in data or 'transaction_type' not in data or 'amount' not in data:
            return jsonify({"error": "Missing required fields: account_id, transaction_type, amount"}), 400
        
        account_id = data.get('account_id')
        transaction_type = data.get('transaction_type')
        amount = data.get('amount')
        description = data.get('description')
        
        if transaction_type not in ['deposit', 'withdrawal']:
            return jsonify({"error": "Invalid transaction type. Must be 'deposit' or 'withdrawal'"}), 400
        
        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Amount must be a positive number"}), 400
        
        db = get_db()
        transaction, error = TransactionService.create_transaction(
            db, account_id, transaction_type, amount, description
        )
        
        if error:
            return jsonify({"error": error}), 400
        
        return jsonify({
            "message": "Transaction created successfully",
            "transaction": transaction.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_bp.route('/transactions', methods=['GET'])
def get_all_transactions():
    try:
        db = get_db()
        transactions = TransactionService.get_all_transactions(db)
        
        return jsonify({
            "transactions": [t.to_dict() for t in transactions],
            "count": len(transactions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        db = get_db()
        transaction = TransactionService.get_transaction_by_id(db, transaction_id)
        
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        return jsonify({"transaction": transaction.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_bp.route('/accounts/<int:account_id>/transactions', methods=['GET'])
def get_transactions_by_account(account_id):

    try:
        db = get_db()
        transactions = TransactionService.get_transactions_by_account(db, account_id)
        
        return jsonify({
            "account_id": account_id,
            "transactions": [t.to_dict() for t in transactions],
            "count": len(transactions)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        db = get_db()
        success = TransactionService.delete_transaction(db, transaction_id)
        
        if not success:
            return jsonify({"error": "Transaction not found"}), 404
        
        return jsonify({"message": "Transaction deleted successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500