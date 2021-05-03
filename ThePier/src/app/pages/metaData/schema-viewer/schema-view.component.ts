import { Component, ElementRef, Input, OnChanges, ViewChild } from '@angular/core';
import { faChevronDown, faChevronRight, faMinus } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'metadata-schema-view',
  templateUrl: './schema-view.component.html',
  styleUrls: ['./schema-view.component.scss'],
})
export class SchemaViewComponent implements OnChanges {
  @Input() public field: any;
  @Input() public flattenName: string;

  @ViewChild('addInput') private addInput: ElementRef;

  public readonly Object = Object;
  public readonly collapsedIcon = faChevronRight;
  public readonly expandedIcon = faChevronDown;
  public readonly removeIcon = faMinus;

  public expanded = false;

  public get type() {
    let t = typeof this.field.type;
    if (t == 'object') {
      return 'object';
    } else {
      return this.field.type;
    }
  }

  public ngOnChanges(): void {}

  public addMetadata() {
    if (this.field.metadata[this.addInput.nativeElement.value] == null) {
      this.field.metadata[this.addInput.nativeElement.value] = '';
      this.addInput.nativeElement.value = null;
    }
  }

  public removeMetadataField(key: string) {
    delete this.field.metadata[key];
  }
}
