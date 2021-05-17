import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

interface Value {
    host: string;
    port: number;
    database: string;
    table: string;
    user: string;
    password: string;
}

@Component({
    selector: 'app-ingestion-postgresql-information',
    templateUrl: './postgresql-information.component.html',
    styleUrls: ['./postgresql-information.component.scss'],
})
export class PostgresqlInformationComponent implements OnInit {
    public form: FormGroup;

    public get invalid() {
        return this.form.invalid;
    }

    constructor(private cdr: ChangeDetectorRef) {}

    ngOnInit(): void {
        this.form = new FormGroup({
            host: new FormControl(null, Validators.required),
            port: new FormControl(5432, Validators.required),
            database: new FormControl('', Validators.required),
            table: new FormControl('', Validators.required),
            user: new FormControl('', Validators.required),
            password: new FormControl('', Validators.required),
        });
    }

    appendToBody(body: FormData) {
        body.append('host', this.form.value.host);
        body.append('port', this.form.value.port.toString());
        body.append('database', this.form.value.database);
        body.append('table', this.form.value.table);
        body.append('user', this.form.value.user);
        body.append('password', this.form.value.password);
    }

    saveState() {
        localStorage.setItem('ingestionPostgresqlInfo', JSON.stringify(this.form.value));
    }

    restoreState() {
        const info = JSON.parse(localStorage.getItem('ingestionPostgresqlInfo'));
        if (info) {
            this.form.setValue(info);
            this.cdr.detectChanges();
        }
    }

    clearState() {
        localStorage.removeItem('ingestionPostgresqlInfo');
    }
}
