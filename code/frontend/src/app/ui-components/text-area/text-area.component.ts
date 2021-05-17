import { Component, forwardRef, Input, OnInit } from '@angular/core';
import { NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';
import { InputComponent } from '../input/input.component';

@Component({
    selector: 'app-text-area',
    templateUrl: './text-area.component.html',
    styleUrls: ['./text-area.component.scss'],
    providers: [{
        provide: NG_VALUE_ACCESSOR,
        useExisting: forwardRef(() => TextAreaComponent),
        multi: true
    }]
})
export class TextAreaComponent implements OnInit, ControlValueAccessor {

    @Input() public disabled: boolean;
    @Input() public label: string;
    @Input() public id: string;
    @Input() public rows: number;
    @Input() public cols: number;
    @Input() public resize: string;

    public value = '';

    private propagateChange: (_: any) => any;

    constructor() { }

    ngOnInit(): void {}

    writeValue(obj: any): void {
        if (obj !== undefined) {
            this.value = obj;
        }
    }

    registerOnChange(fn: any): void {
        this.propagateChange = fn;
    }

    registerOnTouched(fn: any): void {}

    setDisabledState?(isDisabled: boolean): void {
        this.disabled = isDisabled;
    }

    onInput(value: string) {
        this.value = value;
        if (this.propagateChange) {
            this.propagateChange(value);
        }
    }

}
