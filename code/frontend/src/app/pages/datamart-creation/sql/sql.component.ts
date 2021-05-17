import { ChangeDetectorRef, Component, Input, OnInit } from '@angular/core';

@Component({
    selector: 'app-creation-sql',
    templateUrl: './sql.component.html',
    styleUrls: ['./sql.component.scss']
})
export class SqlComponent implements OnInit {

    @Input() disabled: boolean;

    public readonly stateName = 'datamartCreation-sql';

    public sqlCode: string;

    constructor(private cdr: ChangeDetectorRef) { }

    ngOnInit(): void { }

    public saveState() {
        localStorage.setItem(this.stateName, this.sqlCode);
    }

    public loadState() {
        this.sqlCode = localStorage.getItem(this.stateName) ?? '';
        this.cdr.detectChanges();
    }

    public deleteState() {
        localStorage.removeItem(this.stateName);
    }
}
