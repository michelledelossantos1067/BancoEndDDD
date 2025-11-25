import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TransactionService, Transaction } from '../../services/transaction';
import { AccountService, Account } from '../../services/account';

@Component({
  selector: 'app-transaction-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './transaction-list.html',
  styleUrl: './transaction-list.scss'
})
export class TransactionList implements OnInit {
  transactions: Transaction[] = [];
  accounts: Account[] = [];
  newTransaction: Transaction = {
    account_id: 0,
    transaction_type: 'deposit',
    amount: 0,
    description: ''
  };
  showForm = false;
  selectedAccountId: number | null = null;

  constructor(
    private transactionService: TransactionService,
    private accountService: AccountService
  ) { }

  ngOnInit(): void {
    this.loadTransactions();
    this.loadAccounts();
  }

  loadTransactions(): void {
    if (this.selectedAccountId) {
      this.transactionService.getTransactionsByAccount(this.selectedAccountId).subscribe({
        next: (data) => {
          console.log('Transactions loaded:', data);
          this.transactions = data;
        },
        error: (error) => console.error('Error loading transactions:', error)
      });
    } else {
      this.transactionService.getAllTransactions().subscribe({
        next: (data) => {
          console.log('All transactions loaded:', data);
          this.transactions = data;
        },
        error: (error) => console.error('Error loading transactions:', error)
      });
    }
  }

  loadAccounts(): void {
    this.accountService.getAllAccounts().subscribe({
      next: (data) => {
        console.log('Accounts loaded:', data);
        this.accounts = data;
      },
      error: (error) => console.error('Error loading accounts:', error)
    });
  }

  createTransaction(): void {
    // Validar que se haya seleccionado una cuenta
    if (!this.newTransaction.account_id || this.newTransaction.account_id === 0) {
      alert('Por favor seleccione una cuenta');
      return;
    }

    // Validar que el monto sea mayor a 0
    if (!this.newTransaction.amount || this.newTransaction.amount <= 0) {
      alert('El monto debe ser mayor a 0');
      return;
    }

    console.log('Creating transaction:', this.newTransaction);

    this.transactionService.createTransaction(this.newTransaction).subscribe({
      next: (data) => {
        console.log('Transaction created:', data);
        this.loadTransactions();
        this.loadAccounts(); // Recargar para actualizar balances
        this.resetForm();
        this.showForm = false;
        alert('Transacción creada exitosamente');
      },
      error: (error) => {
        console.error('Error creating transaction:', error);
        const errorMsg = error.error?.error || error.message || 'Error desconocido';
        alert('Error: ' + errorMsg);
      }
    });
  }

  deleteTransaction(id: number | undefined): void {
    if (id && confirm('¿Estás seguro de que deseas eliminar esta transacción?')) {
      this.transactionService.deleteTransaction(id).subscribe({
        next: () => {
          this.loadTransactions();
          alert('Transacción eliminada exitosamente');
        },
        error: (error) => console.error('Error deleting transaction:', error)
      });
    }
  }

  filterByAccount(): void {
    this.loadTransactions();
  }

  resetForm(): void {
    this.newTransaction = {
      account_id: 0,
      transaction_type: 'deposit',
      amount: 0,
      description: ''
    };
  }

  getAccountName(accountId: number): string {
    const account = this.accounts.find(acc => acc.id === accountId);
    return account ? account.holder_name : 'Desconocido';
  }

  getTransactionTypeLabel(type: string): string {
    return type === 'deposit' ? 'Depósito' : 'Retiro';
  }
}