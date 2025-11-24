import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '', redirectTo: '/accounts', pathMatch: 'full' },
    { path: 'accounts', component: AccountListComponent },
    { path: 'transactions', component: TransactionListComponent }
];
