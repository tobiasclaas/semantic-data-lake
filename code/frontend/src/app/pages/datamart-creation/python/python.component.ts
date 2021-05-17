import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';

@Component({
    selector: 'app-creation-python',
    templateUrl: './python.component.html',
    styleUrls: ['./python.component.scss']
})
export class PythonComponent implements OnInit {

    @Input() disabled: boolean;

    public readonly stateName = 'datamartCreation-python';

    public pythonCode: string;

    constructor(private cdr: ChangeDetectorRef) { }

    ngOnInit(): void {
    }

    public saveState() {
        localStorage.setItem(this.stateName, this.pythonCode);
    }

    public loadState() {
        this.pythonCode = localStorage.getItem(this.stateName) ?? '';
        this.cdr.detectChanges();
    }

    public deleteState() {
        localStorage.removeItem(this.stateName);
    }
}
