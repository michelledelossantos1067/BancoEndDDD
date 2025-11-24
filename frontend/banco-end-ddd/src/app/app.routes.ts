import { Routes } from '@angular/router';
import { AccountList } from './components/account-list/account-list';

export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'accounts', component: AccountList },
//  { path: 'transactions', component: TransactionList }
];