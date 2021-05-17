import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import '../../../constants';
import { SOURCES, TARGETS } from '../../../constants';

interface Value {
    source: string;
    target: string;
    humanReadableName: string;
    comment: string;
}

@Component({
    selector: 'app-ingestion-common-information',
    templateUrl: './common-information.component.html',
    styleUrls: ['./common-information.component.scss'],
})
export class CommonInformationComponent implements OnInit {
    public form: FormGroup;
    public sources = SOURCES.options;
    public targets = TARGETS.options;

    public get invalid() {
        return this.form.invalid;
    }

    public get source(): string {
        return this.form?.get('source')?.value;
    }

    constructor(private cdr: ChangeDetectorRef) {}

    ngOnInit(): void {
        this.form = new FormGroup({
            source: new FormControl(null, Validators.required),
            target: new FormControl(null, Validators.required),
            humanReadableName: new FormControl('', Validators.required),
            comment: new FormControl('')
        });
    }

    appendToBody(body: FormData) {
        body.append('human_readable_name', this.form.value.humanReadableName);

        let comment: string;
        if ((comment = this.form.value.comment)) {
            body.append('comment', comment);
        }

        let target: string;
        if ((target = this.form.value.target)) {
            body.append('target_storage', target);
        }
    }

    saveState() {
        localStorage.setItem('ingestionCommonInfo', JSON.stringify(this.form.value));
    }

    restoreState() {
        const info = JSON.parse(localStorage.getItem('ingestionCommonInfo'));
        if (info) {
            this.form.setValue(info);
            this.cdr.detectChanges();
        }
    }

    clearState() {
        localStorage.removeItem('ingestionCommonInfo');
    }
}
