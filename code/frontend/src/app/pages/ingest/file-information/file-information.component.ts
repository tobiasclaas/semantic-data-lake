import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { FILE_TYPE } from '../../../constants';

@Component({
    selector: 'app-ingestion-file-information',
    templateUrl: './file-information.component.html',
    styleUrls: ['./file-information.component.scss'],
})
export class FileInformationComponent implements OnInit {
    public form: FormGroup;
    public selectedFile: File;
    public fileType: string;

    public fileContent: string;

    public get invalid() {
        return this.form.invalid;
    }

    constructor(private cdr: ChangeDetectorRef) { }

    ngOnInit(): void {
        this.form = new FormGroup({
            delimiter: new FormControl(null),
            hasHeader: new FormControl(null),
            rowTag: new FormControl(null)
        });
    }

    handleUpload(event) {
        const file = event.target.files[0] as File;

        if (file.name.endsWith('.csv')) {
            this.fileType = FILE_TYPE.csv;
        } else if (file.name.endsWith('.json')) {
            this.fileType = FILE_TYPE.json;
        } else if (file.name.endsWith('.xml')) {
            this.fileType = FILE_TYPE.xml;
        }

        this.selectedFile = new File([file], file.name, { type: this.fileType });
        this.readFile();
    }

    appendToBody(body: FormData) {
        body.append('file', this.selectedFile, this.selectedFile.name);

        if (this.form.value.delimiter) {
            body.append('delimiter', this.form.value.delimiter);
        }

        if (this.form.value.hasHeader) {
            body.append('has_header', this.form.value.hasHeader);
        }

        if (this.form.value.rowTag) {
            body.append('row_tag', this.form.value.rowTag);
        }
    }

    saveState() {
        localStorage.setItem('ingestionFilelInfo', JSON.stringify(this.form.value));
        localStorage.setItem('ingestionFilelInfo-fileType', this.fileType);
        if (this.selectedFile) {
            localStorage.setItem('ingestionFilelInfo-filename', this.selectedFile.name);
            const reader = new FileReader();
            reader.readAsText(this.selectedFile);
            reader.onload = (result) => {
                localStorage.setItem('ingestionFilelInfo-file', result.target.result as string);
            };
        }
    }

    restoreState() {
        this.fileType = localStorage.getItem('ingestionFilelInfo-fileType');

        const content = localStorage.getItem('ingestionFilelInfo-file');
        console.log(this.fileType);
        if (content) {
            this.selectedFile = new File(
                [content],
                localStorage.getItem('ingestionFilelInfo-filename'),
                {
                    type: this.fileType,
                }
            );
            this.readFile();
        }

        const info = JSON.parse(localStorage.getItem('ingestionFilelInfo'));
        if (info) {
            this.form.setValue(info);
            this.cdr.detectChanges();
        }
    }

    clearState() {
        localStorage.removeItem('ingestionFilelInfo-fileType');
        localStorage.removeItem('ingestionFilelInfo-file');
        localStorage.removeItem('ingestionFilelInfo');
    }

    private readFile() {
        const reader = new FileReader();
        reader.readAsText(this.selectedFile);
        reader.onload = (event) => {
            this.fileContent = event.target.result as string;
        };
    }
}
