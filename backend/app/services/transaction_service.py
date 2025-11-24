from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.services.account_service import AccountService

class TransactionService:
    
    @staticmethod
    def create_transaction(db: Session, account_id: int, transaction_type: str, amount: float, description: str = None):
        account = AccountService.get_account_by_id(db, account_id)
        if not account:
            return None, "Account not found"
        
        if transaction_type == "withdrawal":
            if account.balance < amount:
                return None, "Insufficient funds"
            new_balance = account.balance - amount
        elif transaction_type == "deposit":
            new_balance = account.balance + amount
        else:
            return None, "Invalid transaction type"
        
        transaction = Transaction(
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            balance_after=new_balance
        )
        
        db.add(transaction)
        AccountService.update_balance(db, account_id, new_balance)
        db.commit()
        db.refresh(transaction)
        
        return transaction, None

    @staticmethod
    def get_all_transactions(db: Session):
        return db.query(Transaction).all()

    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int):
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def get_transactions_by_account(db: Session, account_id: int):
        return db.query(Transaction).filter(Transaction.account_id == account_id).all()

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int):
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            return False
        
        db.delete(transaction)
        db.commit()
        return True