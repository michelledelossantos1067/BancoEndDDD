import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Transaction {
  id?: number;
  account_id: number;
  transaction_type: string;
  amount: number;
  description?: string;
  balance_after?: number;
  created_at?: string;
}

export interface TransactionResponse {
  transactions: Transaction[];
  count: number;
}

export interface TransactionCreateResponse {
  message: string;
  transaction: Transaction;
}

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getAllTransactions(): Observable<Transaction[]> {
    return this.http.get<TransactionResponse>(`${this.apiUrl}/transactions`).pipe(
      map(response => response.transactions)
    );
  }

  getTransactionById(id: number): Observable<Transaction> {
    return this.http.get<{ transaction: Transaction }>(`${this.apiUrl}/transactions/${id}`).pipe(
      map(response => response.transaction)
    );
  }

  getTransactionsByAccount(accountId: number): Observable<Transaction[]> {
    return this.http.get<TransactionResponse>(`${this.apiUrl}/accounts/${accountId}/transactions`).pipe(
      map(response => response.transactions)
    );
  }

  createTransaction(transaction: Transaction): Observable<Transaction> {
    return this.http.post<TransactionCreateResponse>(`${this.apiUrl}/transactions`, transaction).pipe(
      map(response => response.transaction)
    );
  }

  deleteTransaction(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/transactions/${id}`);
  }
}