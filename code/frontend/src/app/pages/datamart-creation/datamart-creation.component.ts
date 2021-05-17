import { HttpClient } from '@angular/common/http';
import { AfterViewInit, ChangeDetectorRef, Component, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { TARGETS } from 'src/app/constants';
import { environment } from 'src/environments/environment';
import { PreviewComponent } from './preview/preview.component';
import { PythonComponent } from './python/python.component';
import { SelectionComponent } from './selection/selection.component';
import { SqlComponent } from './sql/sql.component';

@Component({
    selector: 'app-datamart-creation',
    templateUrl: './datamart-creation.component.html',
    styleUrls: ['./datamart-creation.component.scss'],
})
export class DatamartCreationComponent implements OnInit, AfterViewInit, OnDestroy {

    @ViewChild(SelectionComponent) selection: SelectionComponent;
    @ViewChild(PythonComponent) python: PythonComponent;
    @ViewChild(SqlComponent) sql: SqlComponent;
    @ViewChild(PreviewComponent) preview: PreviewComponent;

    public readonly targets = TARGETS.options.filter(e => e.value !== TARGETS.sameAsSource);

    public sentSave: boolean;
    public saveForm: FormGroup;

    constructor(private router: Router, private cdr: ChangeDetectorRef, private httpClient: HttpClient) { }

    @HostListener('window:beforeunload', ['$event']) unloadHandler(event: Event) {
        this.saveState();
    };

    public ngOnInit(): void {
        this.saveForm = new FormGroup({
            target: new FormControl(TARGETS.mongodb),
            humanReadableName: new FormControl(null, Validators.required),
            comment: new FormControl('')
        });
    }

    public ngAfterViewInit(): void {
        this.loadState();
    }

    public ngOnDestroy(): void {
        this.saveState();
    }

    public save() {
        if (!this.sentSave) {
            this.sentSave = true;
            this.httpClient
            .post<string>(
                `${environment.backendUrl}/datamarts/creation/save`,
                {
                    datamarts: this.selection.datamarts.map((e) => e.id),
                        // eslint-disable-next-line @typescript-eslint/naming-convention
                        human_readable_name: this.saveForm.value.humanReadableName,
                        comment: this.saveForm.value.comment,
                        // eslint-disable-next-line @typescript-eslint/naming-convention
                        target_storage: this.saveForm.value.target,
                    },
                    { withCredentials: true }
                )
                .subscribe((response) => {
                    this.sentSave = false;
                    this.router.navigate(['/']);
                });
        }
    }

    public cancel() {
        this.selection.deleteState();
        this.python.deleteState();
        this.sql.deleteState();
        this.preview.deleteState();
        this.router.navigate(['/']);
    }

    private saveState() {
        this.selection.saveState();
        this.python.saveState();
        this.sql.saveState();
        this.preview.saveState();
    }

    private loadState() {
        this.selection.loadState();
        this.python.loadState();
        this.sql.loadState();
        this.preview.loadState();
        this.cdr.detectChanges();
    }
}
