import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
    {
        path: 'main',
        loadChildren: () => import('./children/cabinet/cabinet.module').then(module => module.CabinetModule)
    },
    {
        path: '**',
        redirectTo: 'main'
    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
