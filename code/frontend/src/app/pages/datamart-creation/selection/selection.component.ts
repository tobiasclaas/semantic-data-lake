import { HttpClient, HttpParams } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { IDatamart } from 'src/app/state/objects';
import { environment } from 'src/environments/environment';
import { DatamartDef } from '../datamartDef';

interface ComponentState {
    searchString: string;
    selectedDatamarts: DatamartDef[];
}

@Component({
    selector: 'app-creation-selection',
    templateUrl: './selection.component.html',
    styleUrls: ['./selection.component.scss']
})
export class SelectionComponent implements OnInit {

    public readonly stateName = 'datamartCreation-selection';

    public isSearching = false;
    public searchString: string;
    public searchResults$ = new BehaviorSubject<IDatamart[]>([]);
    public selectedDatamarts$ = new BehaviorSubject<DatamartDef[]>([]);
    public invalid = false;

    public get datamarts() {
        return this.selectedDatamarts$.value;
    }

    constructor(private httpClient: HttpClient, private cdr: ChangeDetectorRef) { }

    ngOnInit(): void {  }

    public search() {
        let params;
        if (this.searchString && this.searchString !== '') {
            params = new HttpParams().append('search', this.searchString);
        }
        this.isSearching = true;
        this.httpClient
            .get<{ datamarts: IDatamart[]; total: number }>(`${environment.backendUrl}/datamarts`, {
                withCredentials: true,
                observe: 'response',
                params,
            })
            .subscribe((r) => {
                const notSelectedResults: IDatamart[] = [];
                r.body.datamarts.forEach((metadata) => {
                    const index = this.selectedDatamarts$.value.findIndex(
                        ({ id }) => id === metadata.uid
                    );
                    if (index === -1) {
                        notSelectedResults.push(metadata);
                    }
                });

                this.searchResults$.next(notSelectedResults);
                this.isSearching = false;
            });
    }

    public selectDatamart(index: number) {
        const selected = this.selectedDatamarts$.value;
        const searchResults = this.searchResults$.value;
        selected.push({
            identifier: '',
            id: searchResults[index].uid,
            hnr: searchResults[index].humanReadableName,
        });
        searchResults.splice(index, 1);
        this.searchResults$.next(searchResults);
        this.selectedDatamarts$.next(selected);
        this.invalid = true;
    }

    public unselectDatamart(index: number) {
        const selected = this.selectedDatamarts$.value;
        selected.splice(index, 1);
        this.selectedDatamarts$.next(selected);
        this.search();
    }

    validate() {
        let invalid = false;
        this.selectedDatamarts$.value.forEach(datamart => {
            if (!datamart.identifier || datamart.identifier === '') {
                invalid = true;
            }
        });
        this.invalid = invalid;
    }

    public saveState() {
        const state: ComponentState = {
            searchString: this.searchString,
            selectedDatamarts: this.selectedDatamarts$.value
        };
        localStorage.setItem(this.stateName, JSON.stringify(state));
    }

    public loadState() {
        const stateString = localStorage.getItem(this.stateName);
        if (stateString) {
            const state: ComponentState = JSON.parse(stateString);
            this.searchString = state.searchString;
            this.selectedDatamarts$.next(state.selectedDatamarts);
        }
        this.search();
        this.validate();
        this.cdr.detectChanges();
    }

    public deleteState() {
        localStorage.removeItem(this.stateName);
    }
}
