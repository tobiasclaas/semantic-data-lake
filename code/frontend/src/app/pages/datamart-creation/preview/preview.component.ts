import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { DatamartDef } from '../datamartDef';

interface ComponentState {
    previewCount: number;
    schema: any;
    rows: [];
    error: string;
}

@Component({
    selector: 'app-creation-preview',
    templateUrl: './preview.component.html',
    styleUrls: ['./preview.component.scss']
})
export class PreviewComponent implements OnInit {
    @Input() selectedDatamarts: DatamartDef[];
    @Input() pythonCode: string;
    @Input() sqlCode: string;
    @Input() disabled: boolean;

    public readonly stateName = 'datamartCreation-preview';

    public previewSchema: any;
    public previewRows: any;
    public previewError: string;
    public isGeneratingPreview = false;
    public isPollingPreview = false;
    public previewRowCount = 10;

    constructor(private httpClient: HttpClient, private cdr: ChangeDetectorRef) { }

    ngOnInit(): void {
    }

    public generatePreview() {
        this.isGeneratingPreview = true;
        this.previewError = null;
        const datamarts = {};
        this.selectedDatamarts.forEach((datamart) => {
            datamarts[datamart.identifier] = datamart.id;
        });
        const body = {
            datamarts,
            query: this.sqlCode,
            pyspark: this.pythonCode,
        };
        this.httpClient
            .post(`${environment.backendUrl}/datamarts/creation/preview`, body, {
                withCredentials: true,
                observe: 'response',
            })
            .subscribe(
                ({ status }) => {
                    if (status === 200 || status === 202) {
                        this.pollPreview();
                    }
                },
                (error) => {
                    this.isGeneratingPreview = false;
                },
                () => { }
            );
    }

    saveState() {
        const state: ComponentState = {
            previewCount: this.previewRowCount,
            schema: this.previewSchema,
            rows: this.previewRows,
            error: this.previewError
        };
        localStorage.setItem(this.stateName, JSON.stringify(state));
    }

    loadState() {
        const state: ComponentState = JSON.parse(localStorage.getItem(this.stateName));
        if (state) {
            this.previewRowCount = state.previewCount;
            this.previewError = state.error;
            this.previewSchema = state.schema;
            this.previewRows = state.rows;
            this.cdr.detectChanges();
        }
    }

    deleteState() {
        localStorage.removeItem(this.stateName);
    }

    private pollPreview() {
        if (this.isGeneratingPreview) {
            if (!this.isPollingPreview) {
                this.isPollingPreview = true;
                this.httpClient
                    .get(`${environment.backendUrl}/datamarts/creation/preview`, {
                        withCredentials: true,
                        observe: 'response',
                        params: {
                            previewRowCount: this.previewRowCount.toString(),
                        },
                    })
                    .subscribe(
                        (response) => {
                            this.isPollingPreview = false;

                            if (response.status === 202) {
                                setTimeout(() => this.pollPreview(), 1000);
                            } else if (response.status === 201) {
                                this.previewSchema = response.body['schema'];
                                this.previewRows = response.body['rows'];
                                this.previewError = null;
                                this.isGeneratingPreview = false;
                            }
                        },
                        (error) => {
                            this.previewSchema = null;
                            this.previewRows = null;
                            this.previewError = error.error.message;
                            this.isGeneratingPreview = false;
                            this.isPollingPreview = false;
                        },
                        () => { }
                    );
            }
        } else {
            this.isPollingPreview = false;
        }
    }
}
