import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonComponent } from './button/button.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { RouterModule } from '@angular/router';
import { InputComponent } from './input/input.component';
import { DropDownComponent } from './drop-down/drop-down.component';
import { DropDownOptionComponent } from './drop-down/drop-down-option/drop-down-option.component';
import { TextAreaComponent } from './text-area/text-area.component';
import { CheckboxComponent } from './checkbox/checkbox.component';
import { LoadingOverlayComponent } from './loading-overlay/loading-overlay.component';
import { DividerComponent } from './divider/divider.component';

const COMPONENTS = [
  ButtonComponent,
  InputComponent,
  DropDownComponent,
  DropDownOptionComponent,
  TextAreaComponent,
  CheckboxComponent,
  LoadingOverlayComponent,
  DividerComponent
];

@NgModule({
  declarations: COMPONENTS,
  exports: COMPONENTS,
  imports: [
    CommonModule,
    FontAwesomeModule,
    RouterModule
  ]
})
export class UiComponentsModule { }
