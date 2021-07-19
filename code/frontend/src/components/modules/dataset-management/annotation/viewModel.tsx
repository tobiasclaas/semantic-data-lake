import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
} from "mobx";
import React from "react";
import ContentStore from "../../../../models/contentStore";
import { Field, IDatamart } from "../../../../models/datamarts";
import StoreStatus from "../../../../models/storeStatus.enum";
import workspacesStore from "../../../../stores/workspaces.store";
import View from "./main.component";
import FieldView from "./fieldView.component";

class ViewModel extends ContentStore {
  @observable datamart: IDatamart | null = null;
  @observable field: Field | null = null;
  @observable path: string = "";

  constructor(item: IDatamart) {
    super();
    this.datamart = item;
    makeObservable(this);

    this.initialize(item);
  }

  @action display(field: Field | null, path: string) {
    this.field = field;
    this.path = path;
  }

  @computed get getFieldView() {
    return this.field ? (
      <FieldView viewModel={this} path={this.path} field={this.field} />
    ) : null;
  }

  private async initialize(item: IDatamart) {
    const fields = item.metadata.schema.fields;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
