import { Component, forwardRef, Input, OnInit } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
    selector: 'app-checkbox',
    templateUrl: './checkbox.component.html',
    styleUrls: ['./checkbox.component.scss'],
    providers: [{
        provide: NG_VALUE_ACCESSOR,
        useExisting: forwardRef(() => CheckboxComponent),
        multi: true
    }]
})
export class CheckboxComponent implements OnInit, ControlValueAccessor {

    @Input() label: string;

    public checked: boolean;

    private onTouched: () => {};
    private onChange: (_: any) => {};

    constructor() {}
    
    ngOnInit(): void {}

    writeValue(obj: any): void {
        if (obj !== undefined) {
            this.checked = obj
        }
    }

    registerOnChange(fn: any): void {
        this.onChange = fn;
    }

    registerOnTouched(fn: any): void {
        this.onTouched = fn;
    }

    onClick() {
        this.checked = !this.checked;
        this.onChange(this.checked);
    }
}
