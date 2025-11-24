import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AccountService, Account } from '../../services/account';

@Component({
  selector: 'app-account-list',
  imports: [CommonModule, FormsModule],
  templateUrl: './account-list.html',
  styleUrl: './account-list.scss'
})
export class AccountList implements OnInit {
  accounts: Account[] = [];
  newAccount: Account = {
    holder_name: '',
    holder_id: '',
    account_type: 'savings'
  };
  editingAccount: Account | null = null;
  showForm = false;

  constructor(private accountService: AccountService) { }

  ngOnInit(): void {
    this.loadAccounts();
  }

  loadAccounts(): void {
    this.accountService.getAllAccounts().subscribe({
      next: (data) => this.accounts = data,
      error: (error) => console.error('Error al cargar cuentas:', error)
    });
  }

  createAccount(): void {
    this.accountService.createAccount(this.newAccount).subscribe({
      next: () => {
        this.loadAccounts();
        this.resetForm();
        this.showForm = false;
      },
      error: (error) => console.error('Error al crear la cuenta:', error)
    });
  }

  editAccount(account: Account): void {
    this.editingAccount = { ...account };
  }

  updateAccount(): void {
    if (this.editingAccount && this.editingAccount.id) {
      this.accountService.updateAccount(this.editingAccount.id, {
        holder_name: this.editingAccount.holder_name,
        account_type: this.editingAccount.account_type
      }).subscribe({
        next: () => {
          this.loadAccounts();
          this.editingAccount = null;
        },
        error: (error) => console.error('Error al actualizar la cuenta:', error)
      });
    }
  }

  deleteAccount(id: number | undefined): void {
    if (id && confirm('¿Estás seguro de que quieres eliminar esta cuenta?')) {
      this.accountService.deleteAccount(id).subscribe({
        next: () => this.loadAccounts(),
        error: (error) => console.error('Error al eliminar la cuenta:', error)
      });
    }
  }

  resetForm(): void {
    this.newAccount = {
      holder_name: '',
      holder_id: '',
      account_type: 'savings'
    };
  }

  cancelEdit(): void {
    this.editingAccount = null;
  }
}