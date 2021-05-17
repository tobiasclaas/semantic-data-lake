import { AfterViewInit, ChangeDetectorRef, Component, ContentChildren, forwardRef, HostBinding, Input, OnInit, QueryList } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { DropDownOptionComponent } from './drop-down-option/drop-down-option.component';

@Component({
    selector: 'app-drop-down',
    templateUrl: './drop-down.component.html',
    styleUrls: ['./drop-down.component.scss'],
    providers: [{
        provide: NG_VALUE_ACCESSOR,
        useExisting: forwardRef(() => DropDownComponent),
        multi: true
    }]
})
export class DropDownComponent implements OnInit, AfterViewInit, ControlValueAccessor {

    
    @ContentChildren(DropDownOptionComponent) options!: QueryList<DropDownOptionComponent>;
    
    @Input() public disabled: boolean;
    @Input() public label: string;
    @Input() public id: string;
    
    public selectedLabel = '';
    public selectedValue = '';
    public dropDownOpen = false;

    private onChange: (_: any) => any;
    private onTouched: () => any;
    private viewInited: boolean;

    constructor(private cdr: ChangeDetectorRef) { }


    ngOnInit(): void {
        this.viewInited = false
    }

    ngAfterViewInit(): void {
        this.options.forEach((option) => {
            if (option.value === this.selectedValue) {
                this.selectedLabel = option.value
                this.selectedLabel = option.label
            }
            option.selected.subscribe(() => this.select(option));
        });
        this.cdr.detectChanges()
        this.viewInited = true;
    }

    writeValue(obj: any): void {
        if (obj !== undefined) {
            this.selectedValue = obj;

            if (this.viewInited) {
                this.options.forEach((option) => {
                    if (option.value === this.selectedValue) {
                        this.selectedLabel = option.value
                        this.selectedLabel = option.label
                    }
                });
            }
        }
    }

    registerOnChange(fn: any): void {
        this.onChange = fn;
    }

    registerOnTouched(fn: any): void {
        this.onTouched = fn
    }

    onClick() {
        if (this.onTouched) {
            this.onTouched()
        }
        this.dropDownOpen = !this.dropDownOpen;
        this.cdr.detectChanges()
    }

    select(option: DropDownOptionComponent) {
        this.selectedLabel = option.label;
        this.selectedValue = option.value;
        if (this.onChange) {
            this.onChange(this.selectedValue);
        }
        this.dropDownOpen = false;
    }
}
