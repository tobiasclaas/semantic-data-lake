import { HttpClient } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { CookieService } from 'ngx-cookie-service';
import { BehaviorSubject, Observable } from 'rxjs';
import { SetDatamarts, UpdatePersistentHomeState } from 'src/app/state/actions';
import { IDatamart, IUser } from 'src/app/state/objects';
import { PersistentState } from 'src/app/state/persistent.state';
import { VolatileState } from 'src/app/state/volatile.state';
import { environment } from 'src/environments/environment';
import { IPersistentHomeState } from '../persisten-home.state';

@Component({
    selector: 'app-jobs',
    templateUrl: './datamarts.component.html',
    styleUrls: ['./datamarts.component.scss'],
})
export class DatamartsComponent implements OnInit, OnDestroy {
    public datamarts$: Observable<IDatamart[]>;
    public state$ = new BehaviorSubject<IPersistentHomeState>(null);

    public user: IUser;
    public datamarts: [];
    public menuVisible = false;
    public contextMenuVisible = false;

    public contextMenuX: number;
    public contextMenuY: number;
    public contextDatamartId: string;

    public detailsVisible = false;
    public detailsDatamart: IDatamart;

    public isFetching = false;
    public fetchPeriodically: boolean;

    constructor(
        private store: Store,
        private httpClient: HttpClient,
        private cookiesService: CookieService,
        private router: Router,
        private route: ActivatedRoute
    ) {}

    ngOnInit(): void {
        this.store.select(PersistentState.homeState).subscribe((state) => this.state$.next(state));
        this.store.select(VolatileState.activeUser).subscribe((user) => (this.user = user));
        this.datamarts$ = this.store.select(VolatileState.datamarts);
        this.fetchPeriodically = true;
        this.fetchDatamarts();
    }

    ngOnDestroy(): void {
        this.fetchPeriodically = false;
    }

    openContextMenu(event: MouseEvent, datamartId: string) {
        event.preventDefault();
        this.contextMenuX = event.clientX;
        this.contextMenuY = event.clientY;
        this.contextDatamartId = datamartId;
        this.contextMenuVisible = true;
    }

    closeContextMenu() {
        this.contextDatamartId = null;
        this.contextMenuVisible = false;
    }

    openDetails(datamartId: string) {
        this.router.navigate([datamartId], { relativeTo: this.route });
    }

    openIngestion() {
        this.store.dispatch(
            new UpdatePersistentHomeState({
                ...this.state$.value,
                ingestionVisible: true,
            })
        );
    }

    closeIngestion() {
        this.store.dispatch(
            new UpdatePersistentHomeState({
                ...this.state$.value,
                ingestionVisible: false,
            })
        );
    }

    openDashboard(datamartId: string) {
        const name = this.store.selectSnapshot(VolatileState.datamartsById(datamartId)).humanReadableName;
        window.open(
            environment.backendUrl + '/dashboard/' + datamartId,
            name,
            'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,scrollbars=no'
        );

        this.contextDatamartId = null;
        this.contextMenuVisible = false;
    }

    public delete(uid: string) {
        if (confirm(`Delete job ${uid}?`)) {
            this.isFetching = true;
            this.httpClient
                .delete(`${environment.backendUrl}/datamarts/${uid}`, {
                    withCredentials: true,
                    observe: 'response',
                })
                .subscribe((r) => {
                    this.contextDatamartId = null;
                    this.contextMenuVisible = false;
                    this.fetchDatamarts(true);
                });
        }
    }

    private fetchDatamarts(force = false) {
        if (force || !this.isFetching) {
            this.httpClient
                .get<{ datamarts: []; total }>(`${environment.backendUrl}/datamarts`, {
                    withCredentials: true,
                    observe: 'response',
                })
                .subscribe((response) => {
                    if (response.status === 200) {
                        this.store.dispatch(new SetDatamarts(response.body.datamarts));
                    }
                    this.isFetching = false;
                    if (this.fetchPeriodically) {
                        setTimeout(() => this.fetchDatamarts(), 5000);
                    }
                });
        }
    }
}
