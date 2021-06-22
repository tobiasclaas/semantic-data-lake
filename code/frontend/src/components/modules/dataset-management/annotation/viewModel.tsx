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
import { DataSetType, IDataSet } from "../../../../models/dataset";
import StoreStatus from "../../../../models/storeStatus.enum";
import workspacesStore from "../../../../stores/workspaces.store";
import View from "./main.component";

class ViewModel extends ContentStore {
  datasets: IObservableArray<IDataSet>;

  constructor(item: IDataSet) {
    super();
    this.datasets = observable.array([] as IDataSet[]);
    makeObservable(this);

    this.initialize(item);
  }

  private async initialize(item: IDataSet) {
    this.setStatus(StoreStatus.initializing);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const configs = {
        method: "GET",
        headers: { Accept: "application/json" },
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/datasets`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      const datasets = await response.json();
      this.setDataSets(datasets);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action setDataSets(newValue: IDataSet[]) {
    this.datasets.clear();
    this.datasets.push(...newValue);
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
