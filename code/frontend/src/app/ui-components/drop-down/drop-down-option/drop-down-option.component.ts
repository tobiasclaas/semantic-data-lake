import { Component, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';

@Component({
    selector: 'app-drop-down-option',
    templateUrl: './drop-down-option.component.html',
    styleUrls: ['./drop-down-option.component.scss']
})
export class DropDownOptionComponent implements OnInit {

    @Output() selected = new EventEmitter<DropDownOptionComponent>();

    @Input() label: string;
    @Input() value: any;

    constructor() { }

    @HostListener('click')
    onClick() {
        this.selected.emit(this);
    }

    ngOnInit(): void {
    }

}
