import { Component, forwardRef, Input, OnInit } from '@angular/core';
import { AbstractControl, ControlValueAccessor, NG_VALIDATORS, NG_VALUE_ACCESSOR, ValidationErrors, Validator } from '@angular/forms';
import * as uuid from 'uuid';

@Component({
    selector: 'app-input',
    templateUrl: './input.component.html',
    styleUrls: ['./input.component.scss'],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => InputComponent),
            multi: true
        }
    ]
})
export class InputComponent implements OnInit, ControlValueAccessor {

    @Input() public disabled: boolean;
    @Input() public label: string;
    @Input() public id: string;
    @Input() public type = 'text';
    @Input() public prefix: string;
    @Input() public prefixedValue: boolean;
    @Input() public iconLeft: string;
    @Input() public iconRight: string;
    @Input() public value = '';

    private propagateChange: (_: any) => any;
    private touched: () => any;

    constructor() { }

    ngOnInit(): void {
        if (!this.id) {
            this.id = uuid.v4();
        }
    }

    writeValue(obj: any): void {
        if (obj !== undefined) {
            if (this.prefixedValue) {
                obj = this.prefix + obj;
            }
            this.value = obj;
        }
    }

    registerOnChange(fn: any): void {
        this.propagateChange = fn;
    }

    registerOnTouched(fn: any): void {
        this.touched = fn;
    }

    setDisabledState?(isDisabled: boolean): void {
        this.disabled = isDisabled;
    }

    onInput(value: string) {
        if (this.prefixedValue) {
            value = this.prefix + value;
        }
        this.value = value;
        if (this.propagateChange) {
            this.propagateChange(value);
        }
        if (this.touched) {
            this.touched();
        }
    }
}
