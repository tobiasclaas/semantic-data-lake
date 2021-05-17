import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NgxsReduxDevtoolsPluginModule } from '@ngxs/devtools-plugin';
import { NgxsStoragePluginModule } from '@ngxs/storage-plugin';
import { NgxsModule } from '@ngxs/store';
import { CookieService } from 'ngx-cookie-service';
import { environment } from 'src/environments/environment';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DatamartCreationComponent } from './pages/datamart-creation/datamart-creation.component';
import { DatamartDetailsComponent } from './pages/datamart-details/datamart-details.component';
import { DatamartsComponent } from './pages/home/datamarts/datamarts.component';
import { IngestionComponent } from './pages/ingest/ingestion.component';
import { HomeComponent } from './pages/home/home.component';
import { SchemaViewComponent } from './pages/home/schema-viewer/schema-view.component';
import { LoginComponent } from './pages/login/login.component';
import { UsersComponent } from './pages/users/users.component';
import { PersistentState } from './state/persistent.state';
import { VolatileState } from './state/volatile.state';
import { UiComponentsModule } from './ui-components/ui-components.module';
import { CommonInformationComponent } from './pages/ingest/common-information/common-information.component';
import { MongodbInformationComponent } from './pages/ingest/mongodb-information/mongodb-information.component';
import { PostgresqlInformationComponent } from './pages/ingest/postgresql-information/postgresql-information.component';
import { FileInformationComponent } from './pages/ingest/file-information/file-information.component';
import { SelectionComponent } from './pages/datamart-creation/selection/selection.component';
import { PythonComponent } from './pages/datamart-creation/python/python.component';
import { SqlComponent } from './pages/datamart-creation/sql/sql.component';
import { PreviewComponent } from './pages/datamart-creation/preview/preview.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    IngestionComponent,
    SchemaViewComponent,
    UsersComponent,
    DatamartCreationComponent,
    HomeComponent,
    DatamartDetailsComponent,
    DatamartsComponent,
    CommonInformationComponent,
    MongodbInformationComponent,
    PostgresqlInformationComponent,
    FileInformationComponent,
    SelectionComponent,
    PythonComponent,
    SqlComponent,
    PreviewComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,

    NgxsModule.forRoot([VolatileState, PersistentState], {
      developmentMode: !environment.production,
    }),
    NgxsStoragePluginModule.forRoot({
      key: [PersistentState],
    }),
    NgxsReduxDevtoolsPluginModule.forRoot(),

    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,

    UiComponentsModule,
    FontAwesomeModule,
  ],
  providers: [CookieService],
  bootstrap: [AppComponent],
})
export class AppModule {}
