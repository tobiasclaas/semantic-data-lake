import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
  runInAction,
} from "mobx";
import React from "react";
import ContentStore from "../../../../models/contentStore";
import { IDatamart } from "../../../../models/datamarts";
import StoreStatus from "../../../../models/storeStatus.enum";
import workspacesStore from "../../../../stores/workspaces.store";
import View from "./main.component";

class ViewModel extends ContentStore {
  datamarts: IObservableArray<IDatamart>;

  constructor(item: IDatamart) {
    super();
    this.datamarts = observable.array([] as IDatamart[]);
    makeObservable(this);

    this.initialize(item);
  }

  private async initialize(item: IDatamart) {
    this.setStatus(StoreStatus.initializing);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const configs = {
        method: "GET",
        headers: { Accept: "application/json" },
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/datamarts`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      const datamarts = await response.json();
      this.setDatamarts(datamarts);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action setDatamarts(newValue: IDatamart[]) {
    this.datamarts.clear();
    this.datamarts.push(...newValue);
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
