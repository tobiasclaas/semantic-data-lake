import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
    selector: 'app-button',
    templateUrl: './button.component.html',
    styleUrls: ['./button.component.scss'],
})
export class ButtonComponent implements OnInit {

    @Input() disabled: boolean;
    @Input() routerLink;
    @Input() text: string;
    @Input() icon: string;

    public hasIcon = false;
    public iconOnly = false;

    constructor() {}

    ngOnInit(): void {
        this.icon = this.icon?.trim();
        this.text = this.text?.trim();

        this.hasIcon = this.icon && this.icon !== '';
        this.iconOnly = this.hasIcon && (!this.text || this.text === '');
    }
}
