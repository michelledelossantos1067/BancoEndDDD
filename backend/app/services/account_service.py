from sqlalchemy.orm import Session
from app.models.account import Account
import random
import string

class AccountService:
    
    @staticmethod
    def generate_account_number():
        return ''.join(random.choices(string.digits, k=12))

    @staticmethod
    def create_account(db: Session, holder_name: str, holder_id: str, account_type: str):
        account_number = AccountService.generate_account_number()
        
        while db.query(Account).filter(Account.account_number == account_number).first():
            account_number = AccountService.generate_account_number()
        
        account = Account(
            account_number=account_number,
            holder_name=holder_name,
            holder_id=holder_id,
            account_type=account_type,
            balance=0.0
        )
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_all_accounts(db: Session):
        return db.query(Account).all()

    @staticmethod
    def get_account_by_id(db: Session, account_id: int):
        return db.query(Account).filter(Account.id == account_id).first()

    @staticmethod
    def get_account_by_number(db: Session, account_number: str):
        return db.query(Account).filter(Account.account_number == account_number).first()

    @staticmethod
    def update_account(db: Session, account_id: int, holder_name: str = None, account_type: str = None):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return None
        
        if holder_name:
            account.holder_name = holder_name
        if account_type:
            account.account_type = account_type
        
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def delete_account(db: Session, account_id: int):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return False
        
        db.delete(account)
        db.commit()
        return True

    @staticmethod
    def update_balance(db: Session, account_id: int, new_balance: float):
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return None
        
        account.balance = new_balance
        db.commit()
        db.refresh(account)
        return account