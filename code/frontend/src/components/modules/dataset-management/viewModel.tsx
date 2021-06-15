import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
  runInAction,
} from "mobx";
import React from "react";
import ContentStore from "../../../models/contentStore";
import { DataSetType, IDataSet } from "../../../models/dataset";
import StoreStatus from "../../../models/storeStatus.enum";
import routingStore from "../../../stores/routing.store";
import workspacesStore from "../../../stores/workspaces.store";
import BodyViewModel from "./body/bodyViewModel";
import View from "./main.component";

class ViewModel extends ContentStore {
  datasets: IObservableArray<IDataSet>;

  constructor() {
    super();
    this.datasets = observable.array([] as IDataSet[]);
    makeObservable(this);

    this.initialize();
  }

  private async initialize() {
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

  // Upload Modal

  @observable isUploadDialogOpen: boolean = false;
  @action openUploadDialog() {
    this.isUploadDialogOpen = true;
    this.uploadName = "";
    this.setUploadType(DataSetType.csv);
  }
  @action closeUploadDialog() {
    this.isUploadDialogOpen = false;
    this.setUploadType(DataSetType.csv);
    this.uploadName = "";
  }

  @observable uploadName: string = "";
  @action setUploadName(value: string) {
    this.uploadName = value;
  }

  @observable bodyContentViewModel: BodyViewModel | null = null;
  @observable uploadType: DataSetType = DataSetType.csv;
  @action async setUploadType(value: DataSetType) {
    this.uploadType = value;
    await import("./body/" + this.uploadType).then(
      (res) => (this.bodyContentViewModel = new res.default() as BodyViewModel)
    );
  }

  @computed get bodyView() {
    if (!this.bodyContentViewModel) return null;
    return this.bodyContentViewModel.getView();
  }

  @observable uploadFile: File | null = null;
  @action setUploadFile(value: File | null) {
    this.uploadFile = value;
  }

  @computed get canUpload(): boolean {
    return (
      this.uploadName.length > 0 &&
      this.bodyContentViewModel != null &&
      this.bodyContentViewModel.canUpload()
    );
  }

  async upload() {
    this.setStatus(StoreStatus.working);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");
      const formData = new FormData();
      formData.append("name", this.uploadName);
      formData.append("file", this.uploadFile as Blob);

      const configs = {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        body: formData,
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/datasets`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      runInAction(async () => {
        this.datasets.push((await response.json()) as IDataSet);
      });
      this.closeUploadDialog();
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  async delete(item: IDataSet) {
    this.setStatus(StoreStatus.working);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const configs = {
        method: "DELETE",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/datasets/${item.id}`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      this.datasets.remove(item);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
