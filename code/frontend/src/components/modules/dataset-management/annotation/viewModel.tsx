import { IObservableArray, makeObservable, observable } from "mobx";
import React from "react";
import ContentStore from "../../../../models/contentStore";
import { IDatamart } from "../../../../models/datamarts";
import StoreStatus from "../../../../models/storeStatus.enum";
import workspacesStore from "../../../../stores/workspaces.store";
import View from "./main.component";

class ViewModel extends ContentStore {
  @observable datamart: IDatamart | null = null;
  constructor(item: IDatamart) {
    super();
    this.datamart = item;
    makeObservable(this);

    this.initialize(item);
  }

  private async initialize(item: IDatamart) {
    const fields = item.metadata.schema.fields;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
