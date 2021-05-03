import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginGuard } from './login.guard';
import { DatamartCreationComponent } from './pages/datamart-creation/datamart-creation.component';
import { JobsComponent } from './pages/jobs/jobs.component';
import { LoginComponent } from './pages/login/login.component';
import { MetaDataComponent } from './pages/metaData/meta-data.component';
import { UsersComponent } from './pages/users/users.component';

const routes: Routes = [
  { path: '', redirectTo: '/dataMarts', pathMatch: 'full' },
  { path: 'login', component: LoginComponent, canActivate: [LoginGuard] },
  { path: 'users', component: UsersComponent, canActivate: [LoginGuard] },
  { path: 'jobs', component: JobsComponent, canActivate: [LoginGuard] },
  {
    path: 'dataMarts',
    canActivate: [LoginGuard],
    children: [
      { path: '', component: MetaDataComponent },
      { path: 'creation', component: DatamartCreationComponent },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
