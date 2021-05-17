import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

interface Value {
    host: string;
    port: number;
    database: string;
    collection: string;
    user: string;
    password: string;
}

@Component({
    selector: 'app-ingestion-mongodb-information',
    templateUrl: './mongodb-information.component.html',
    styleUrls: ['./mongodb-information.component.scss'],
})
export class MongodbInformationComponent implements OnInit {
    public form: FormGroup;

    public get invalid() {
        return this.form.invalid;
    }

    constructor(private cdr: ChangeDetectorRef) {}

    ngOnInit(): void {
        this.form = new FormGroup({
            host: new FormControl(null, Validators.required),
            port: new FormControl(27017, Validators.required),
            database: new FormControl('', Validators.required),
            collection: new FormControl('', Validators.required),
            user: new FormControl(''),
            password: new FormControl(''),
        });
    }

    appendToBody(body: FormData) {
        body.append('host', this.form.value.host);
        body.append('port', this.form.value.port.toString());
        body.append('database', this.form.value.database);
        body.append('collection', this.form.value.collection);
        body.append('user', this.form.value.user);
        body.append('password', this.form.value.password);
    }

    saveState() {
        localStorage.setItem('ingestionMongodbInfo', JSON.stringify(this.form.value));
    }

    restoreState() {
        const info = JSON.parse(localStorage.getItem('ingestionMongodbInfo'));
        if (info) {
            this.form.setValue(info);
            this.cdr.detectChanges();
        }
    }

    clearState() {
        localStorage.removeItem('ingestionMongodbInfo');
    }
}
