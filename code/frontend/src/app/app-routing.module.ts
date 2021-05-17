import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginGuard } from './login.guard';
import { DatamartCreationComponent } from './pages/datamart-creation/datamart-creation.component';
import { DatamartDetailsComponent } from './pages/datamart-details/datamart-details.component';
import { DatamartsComponent } from './pages/home/datamarts/datamarts.component';
import { HomeComponent } from './pages/home/home.component';
import { IngestionComponent } from './pages/ingest/ingestion.component';
import { LoginComponent } from './pages/login/login.component';
import { UsersComponent } from './pages/users/users.component';

const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
        canActivate: [LoginGuard],
        children: [
            { path: '', redirectTo: '/datamarts', pathMatch: 'full' },
            { path: 'datamarts', component: DatamartsComponent },
            { path: 'users', component: UsersComponent },
        ],
    },
    { path: 'login', component: LoginComponent, canActivate: [LoginGuard] },
    { path: 'datamarts/ingest', component: IngestionComponent, canActivate: [LoginGuard]  },
    { path: 'datamarts/create', component: DatamartCreationComponent, canActivate: [LoginGuard]  },
    { path: 'datamarts/:id', component: DatamartDetailsComponent, canActivate: [LoginGuard]  },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
    exports: [RouterModule],
})
export class AppRoutingModule {}
