import {
    Component,
    ElementRef,
    Input,
    OnChanges,
    SimpleChange,
    SimpleChanges,
    ViewChild,
} from '@angular/core';
import { faChevronDown, faChevronRight, faMinus } from '@fortawesome/free-solid-svg-icons';
import { Store } from '@ngxs/store';
import { PersistentState } from 'src/app/state/persistent.state';
import { VolatileState } from 'src/app/state/volatile.state';

@Component({
    selector: 'metadata-schema-view',
    templateUrl: './schema-view.component.html',
    styleUrls: ['./schema-view.component.scss'],
})
export class SchemaViewComponent implements OnChanges {
    @Input() public field: any;
    @Input() public flattenName: string;
    @Input() public editable = false;

    @ViewChild('addInput') private addInput: ElementRef;

    public readonly Object = Object;
    public readonly collapsedIcon = faChevronRight;
    public readonly expandedIcon = faChevronDown;
    public readonly removeIcon = faMinus;

    public expanded = false;

    public datamartId = ""

    private changes = new Map<string, {}>();

    constructor(private store: Store) {
        this.store.select(PersistentState.homeState).subscribe(({detialsDatamartId}) => {
            if (this.datamartId != detialsDatamartId) {
                this.changes = new Map<string, {}>();
                this.datamartId = detialsDatamartId;
            }
        })
    }

    public get type() {
        let t = typeof this.field.type;
        if (t == 'object') {
            return 'object';
        } else {
            return this.field.type;
        }
    }

    public ngOnChanges(changes: SimpleChanges): void {
        if (changes.field) {
            this.changes.forEach((value, key) => {
                switch (value['type']) {
                    case 0:
                        changes.field.currentValue.metadata[key] = ''
                        break;
                    case 1:
                        changes.field.currentValue.metadata[key] =value['value']
                        break;
                    case 2:
                        changes.field.currentValue.metadata[key];
                        break;
                }
            });
        }
    }

    public editMetadata(key, value) {
        this.changes.set(key, { type: 1, value });
    }

    public addMetadata() {
        const key = this.addInput.nativeElement.value;

        if (this.field.metadata[key] == null) {
            this.field.metadata[key] = '';
            this.addInput.nativeElement.value = null;
            this.changes.set(key, { type: 0 });
        }
    }

    public removeMetadataField(key: string) {
        this.changes.set(key, { type: 2 });
        delete this.field.metadata[key];
    }

    public resetChanges() {
        this.changes = new Map<string, {}>();
        let schema = this.store.selectSnapshot(VolatileState.datamartsById(this.datamartId)).metadata.schema
        let metadata = schema.fields.find(({name}) => name == this.field.name ).metadata
        this.field.metadata = metadata
        this.expanded = false;
    }
}
