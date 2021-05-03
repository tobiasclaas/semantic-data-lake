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
import { NgxJsonViewerModule } from 'ngx-json-viewer';
import { ButtonModule } from 'primeng/button';
import { CheckboxModule } from 'primeng/checkbox';
import { DialogModule } from 'primeng/dialog';
import { DividerModule } from 'primeng/divider';
import { DropdownModule } from 'primeng/dropdown';
import { FieldsetModule } from 'primeng/fieldset';
import { FileUploadModule } from 'primeng/fileupload';
import { InputMaskModule } from 'primeng/inputmask';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputSwitchModule } from 'primeng/inputswitch';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { PanelModule } from 'primeng/panel';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { SelectButtonModule } from 'primeng/selectbutton';
import { TableModule } from 'primeng/table';
import { ToggleButtonModule } from 'primeng/togglebutton';
import { environment } from 'src/environments/environment';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AppbarComponent } from './components/appbar/appbar.component';
import { DatamartCreationComponent } from './pages/datamart-creation/datamart-creation.component';
import { IngestionComponent } from './pages/jobs/components/ingest/ingestion.component';
import { JobsComponent } from './pages/jobs/jobs.component';
import { LoginComponent } from './pages/login/login.component';
import { MetaDataComponent } from './pages/metaData/meta-data.component';
import { SchemaViewComponent } from './pages/metaData/schema-viewer/schema-view.component';
import { UsersComponent } from './pages/users/users.component';
import { PersistentState } from './state/persistent.state';
import { VolatileState } from './state/volatile.state';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    JobsComponent,
    IngestionComponent,
    MetaDataComponent,
    AppbarComponent,
    SchemaViewComponent,
    UsersComponent,
    DatamartCreationComponent
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

    // prime-ng
    PanelModule,
    InputTextModule,
    ButtonModule,
    DropdownModule,
    InputTextareaModule,
    InputMaskModule,
    InputNumberModule,
    InputSwitchModule,
    TableModule,
    FileUploadModule,
    ProgressSpinnerModule,
    CheckboxModule,
    FileUploadModule,
    DividerModule,
    FieldsetModule,
    SelectButtonModule,
    ScrollPanelModule,
    DialogModule,
    ToggleButtonModule,

    NgxJsonViewerModule,

    FontAwesomeModule,
  ],
  providers: [CookieService],
  bootstrap: [AppComponent],
})
export class AppModule {}
