import { HttpClient, HttpEventType } from '@angular/common/http';
import {
    AfterViewInit,
    ChangeDetectorRef,
    Component,
    HostListener,
    OnDestroy,
    ViewChild,
} from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { CommonInformationComponent } from './common-information/common-information.component';
import { FileInformationComponent } from './file-information/file-information.component';
import { FILE_TYPE, SOURCES } from '../../constants';
import { MongodbInformationComponent } from './mongodb-information/mongodb-information.component';
import { PostgresqlInformationComponent } from './postgresql-information/postgresql-information.component';

@Component({
    selector: 'app-ingestion',
    templateUrl: './ingestion.component.html',
    styleUrls: ['./ingestion.component.scss'],
})
export class IngestionComponent implements AfterViewInit, OnDestroy {
    @ViewChild(CommonInformationComponent) commonInfo: CommonInformationComponent;
    @ViewChild(MongodbInformationComponent) mongoInfo: MongodbInformationComponent;
    @ViewChild(PostgresqlInformationComponent) pgInfo: PostgresqlInformationComponent;
    @ViewChild(FileInformationComponent) fileInfo: FileInformationComponent;

    public readonly mongodbSource = SOURCES.mongodb;
    public readonly postgresqlSource = SOURCES.postgresql;
    public readonly fileSource = SOURCES.file;

    constructor(
        private httpClient: HttpClient,
        private cdr: ChangeDetectorRef,
        private router: Router
    ) {}

    @HostListener('window:beforeunload', ['$event']) unloadHandler(event: Event) {
        this.saveState();
    }

    ngAfterViewInit(): void {
        this.restoreState();
    }

    ngOnDestroy(): void {
        this.clearState();
    }

    public ingest() {
        const body: FormData = new FormData();
        let path = '/datamarts/ingestion/';

        switch (this.commonInfo.source) {
            case this.mongodbSource:
                path += 'mongodb';
                this.mongoInfo.appendToBody(body);
                break;

            case this.postgresqlSource:
                path += 'postgres';
                this.pgInfo.appendToBody(body);
                break;

            case this.fileSource:
                this.fileInfo.appendToBody(body);
                switch (this.fileInfo.fileType) {
                    case FILE_TYPE.csv:
                        path += 'csv';
                        break;
                    case FILE_TYPE.json:
                        path += 'json';
                        break;
                    case FILE_TYPE.xml:
                        path += 'xml';
                        break;
                }
                break;
        }

        this.commonInfo.appendToBody(body);

        this.httpClient
            .post(environment.backendUrl + path, body, {
                withCredentials: true,
                observe: 'events',
                reportProgress: true,
            })
            .subscribe((event) => {
                if (event.type === HttpEventType.Response) {
                    if (event.status === 200) {
                        this.router.navigate(['/']);
                    }
                }
            });
    }

    private saveState() {
        this.commonInfo.saveState();
        this.mongoInfo.saveState();
        this.pgInfo.saveState();
        this.fileInfo.saveState();
    }

    private restoreState() {
        this.commonInfo.restoreState();
        this.mongoInfo.restoreState();
        this.pgInfo.restoreState();
        this.fileInfo.restoreState();
        this.cdr.detectChanges();
    }

    private clearState() {
        this.commonInfo.clearState();
        this.mongoInfo.clearState();
        this.pgInfo.clearState();
        this.fileInfo.clearState();
    }
}
