import { HttpClient, HttpEventType, HttpParams } from '@angular/common/http';
import { Component, EventEmitter, OnDestroy, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
import * as moment from 'moment';
import { AddJob } from 'src/app/state/actions';
import { IJob, IngestionType, JobStates } from 'src/app/state/objects';
import { VolatileState } from 'src/app/state/volatile.state';
import { environment } from 'src/environments/environment';
import { HighlightSpanKind } from 'typescript';

@Component({
  selector: 'app-ingestion',
  templateUrl: './ingestion.component.html',
  styleUrls: ['./ingestion.component.scss'],
})
export class IngestionComponent implements OnDestroy {
  @Output() closeIngestion = new EventEmitter();

  public sourceStorages = [
    { label: '--', value: null},
    { label: 'MongoDB', value: 'MongoDB'},
    { label: 'PostgreSQL', value: 'PostgreSQL'},
    { label: 'File', value: 'File'},
  ];
  public targetStorages = [
    { label: 'Same as Source', value: null},
    { label: 'MongoDB', value: 'MongoDB'},
    { label: 'PostgreSQL', value: 'PostgreSQL'},
    { label: 'HDFS', value: 'HDFS'},
  ];

  public commonForm: FormGroup;
  public mongodbForm: FormGroup;
  public postgresForm: FormGroup;
  public fileForm: FormGroup;

  public selectedFile: File;
  public fileType: string;

  constructor(private store: Store, private router: Router, private httpClient: HttpClient) {
    this.createForms();
  }

  public ngOnDestroy(): void { }

  public handleUpload(event)  {
    const file = event.target.files[0] as File;
    this.fileType = file.type;
    if (file.name.endsWith('.csv')) {
      this.fileType = 'text/csv';
    } else if (file.name.endsWith('.xml')) {
      this.fileType = 'application/xml';
    }
    this.selectedFile = new File([file], file.name, { type: this.fileType });
    const fileNameArray = file.name.split('.')
    console.log(this.fileType)
  }

  public ingest() {
    const body: FormData = new FormData();
    let path: string;

    switch (this.commonForm.get('sourceStorage').value) {
      case 'MongoDB':
        const mongodb = this.mongodbForm.value;
        path = '/ingestion/mongodb';
        body.append('host', mongodb.host);
        body.append('port', mongodb.port);
        body.append('database', mongodb.database);
        body.append('collection', mongodb.collection);
        body.append('user', mongodb.user);
        body.append('password', mongodb.password);
        break;

      case 'PostgreSQL':
        const postgresql = this.postgresForm.value;
        path = '/ingestion/postgres';
        body.append('host', postgresql.host);
        body.append('port', postgresql.port);
        body.append('database', postgresql.database);
        body.append('table', postgresql.table);
        body.append('user', postgresql.user);
        body.append('password', postgresql.password);
        break;

      case 'File':
        body.append('file', this.selectedFile, this.selectedFile.name);
        if ( this.fileForm.get('delimiter').value)
          body.append('delimiter', this.fileForm.get('delimiter').value);
        
        if ( this.fileForm.get('hasHeader').value)
          body.append('hasHeader', this.fileForm.get('hasHeader').value);
          
        if ( this.fileForm.get('rowTag').value)
          body.append('rowTag', this.fileForm.get('rowTag').value);
        path = '/ingestion/file';
        break;
    }

    if (this.commonForm.get('comment').value) {
      body.append('comment', this.commonForm.get('humanReadableName').value);
    }

    if (this.commonForm.get('humanReadableName').value) {
      body.append('humanReadableName', this.commonForm.get('humanReadableName').value);
    }

    console.log(this.commonForm.get("targetStorage"))
    if (this.commonForm.get('targetStorage').value) {
      body.append('targetStorageSystem', this.commonForm.get('targetStorage').value);
    }

    console.log(body.get("targetStorageSystem"))
    this.httpClient
      .post<{ jobID: string }>(environment.backendUrl + path, body, {
        withCredentials: true,
        observe: 'events',
        reportProgress: true,
      })
      .subscribe((event) => {
        if (event.type === HttpEventType.Response) {
          if (event.status === 200) {
            if (event.body.jobID) {
              this.store.dispatch(new AddJob(this.createJob(event.body.jobID)));
              this.closeIngestion.emit();
            }
          }
        }
      });
  }

  public restoreState(state: any) {
    if (state == null) {
      return;
    }
    this.commonForm.setValue(state.commonForm);
    this.mongodbForm.setValue(state.mongodbForm);
    this.postgresForm.setValue(state.postgresForm);
    this.fileForm.setValue(state.fileForm);
  }

  public persistState() {
    const state = {
      commonForm: this.commonForm?.value,
      mongodbForm: this.mongodbForm?.value,
      postgresForm: this.postgresForm?.value,
      fileForm: this.fileForm?.value,
    };
    return state;
  }

  private createForms() {
    this.commonForm = new FormGroup({
      sourceStorage: new FormControl('', Validators.required),
      targetStorage: new FormControl('', Validators.required),
      comment: new FormControl(''),
      humanReadableName: new FormControl(''),
    });

    this.mongodbForm = new FormGroup({
      host: new FormControl(null, Validators.required),
      port: new FormControl(27017, Validators.required),
      database: new FormControl('', Validators.required),
      collection: new FormControl('', Validators.required),
      user: new FormControl(''),
      password: new FormControl(''),
    });

    this.postgresForm = new FormGroup({
      host: new FormControl('', Validators.required),
      port: new FormControl(5432, Validators.required),
      database: new FormControl('', Validators.required),
      table: new FormControl('', Validators.required),
      user: new FormControl(''),
      password: new FormControl(''),
    });

    this.fileForm = new FormGroup({
      file: new FormControl('', Validators.required),
      delimiter: new FormControl(''),
      hasHeader: new FormControl(false), 
      rootTag: new FormControl(''),
      rowTag: new FormControl(''),
    });
  }

  private createJob(uid: string): IJob {
    const activeUser = this.store.selectSnapshot(VolatileState.activeUser);
    return {
      uid,
      startedBy: `${activeUser.firstname} ${activeUser.lastname}`,
      startedAt: moment(),
      state: JobStates.started,
      errorMessage: '',
      task: '',
      endedAt: null,
    };
  }
}
