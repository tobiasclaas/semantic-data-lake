import { HttpClient } from '@angular/common/http';
import { Component, Input, OnDestroy, OnInit, ViewChildren } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngxs/store';
import * as moment from 'moment';
import { BehaviorSubject, combineLatest, merge, Subscription, zip } from 'rxjs';
import { combineAll } from 'rxjs/operators';
import { SetDatamarts, UpdatePersistentHomeState } from 'src/app/state/actions';
import { IDatamart } from 'src/app/state/objects';
import { PersistentState } from 'src/app/state/persistent.state';
import { VolatileState } from 'src/app/state/volatile.state';
import { environment } from 'src/environments/environment';
import { SchemaViewComponent } from '../home/schema-viewer/schema-view.component';

@Component({
    selector: 'app-datamart-details',
    templateUrl: './datamart-details.component.html',
    styleUrls: ['./datamart-details.component.scss'],
})
export class DatamartDetailsComponent implements OnInit, OnDestroy {
    public datamart$ = new BehaviorSubject<IDatamart>(null);

    public editable = false;
    public isFetching = false;

    @ViewChildren(SchemaViewComponent) annotations: SchemaViewComponent[];

    public editedHnr = null;
    public editedComment = null;
    public originalHnr = null;
    public originalComment = null;

    private id: string;
    private fetch = false;

    constructor(
        private store: Store,
        private httpClient: HttpClient,
        private route: ActivatedRoute
    ) {}

    ngOnInit(): void {
        this.route.params.subscribe((p) => (this.id = p['id']));
        this.datamart$.subscribe((datamart) => {
            if (datamart) {
                this.originalHnr = datamart.humanReadableName;
                this.originalComment = datamart.comment;

                if (this.editedHnr != null) {
                    this.datamart$.value.humanReadableName = this.editedHnr;
                }

                if (this.editedComment != null) {
                    this.datamart$.value.comment = this.editedComment;
                }
            }
        });
        this.fetch = true;
        this.fetchDatamart();
    }

    ngOnDestroy(): void {
        this.fetch = false
    }

    close() {
        this.store.dispatch(
            new UpdatePersistentHomeState({
                ingestionVisible: false,
                detailsVisible: false,
                detialsDatamartId: null,
            })
        );
    }

    trackEntry(index: number, entry) {
        return entry.uid;
    }

    saveChanges(datamart: IDatamart) {
        this.editable = false;
        if (confirm(`overwrite metadata for ${datamart.humanReadableName ?? datamart.uid}?`)) {
            this.isFetching = true;

            let payload = {
                annotated_schema: datamart.metadata.schema,
                human_readable_name: datamart.humanReadableName,
            };

            if (datamart.comment && datamart.comment != '') {
                payload['comment'] = datamart.comment;
            }

            this.httpClient
                .put<IDatamart>(`${environment.backendUrl}/datamarts/${datamart.uid}`, payload, {
                    withCredentials: true,
                    observe: 'response',
                })
                .subscribe(() => (this.isFetching = false));
        }
    }

    cancel() {
        this.isFetching = true;
        this.annotations.forEach((annotation) => annotation.resetChanges());
        this.editable = false;
        this.editedHnr = null;
        this.editedComment = null;
        this.datamart$.value.humanReadableName = this.originalHnr;
        this.datamart$.value.comment = this.originalComment;
        this.datamart$.next(this.datamart$.value);
        this.isFetching = false;
    }

    openDashboard(datamartId, datamartName) {
        window.open(
            environment.backendUrl + '/dashboard/' + datamartId,
            datamartName,
            'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no'
        );
    }

    private fetchDatamart() {
        if (this.fetch) {
            if (this.id) {
                this.httpClient
                    .get<IDatamart>(`${environment.backendUrl}/datamarts/${this.id}`, {
                        withCredentials: true,
                        observe: 'response',
                    })
                    .subscribe((response) => {
                        if (response.status === 200) {
                            let dm = response.body
                            dm.metadata.createdAt = moment(dm.metadata.createdAt)
                            dm.status.started = moment(dm.status.started)
                            dm.status.ended = moment(dm.status.ended)
                            this.datamart$.next(dm);
                        }
    
                        setTimeout(() => this.fetchDatamart(), 5000);
                    });
            } else {
                setTimeout(() => this.fetchDatamart(), 5000);
            }
        }
    }
}
