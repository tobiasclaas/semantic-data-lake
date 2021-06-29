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
import {
  DatamartStatus,
  DatamartType,
  IDatamart,
} from "../../../models/datamarts";
import StoreStatus from "../../../models/storeStatus.enum";
import routingStore from "../../../stores/routing.store";
import workspacesStore from "../../../stores/workspaces.store";
import BodyViewModel from "./body/bodyViewModel";
import AnnotationViewModel from "./annotation";

import View from "./main.component";

class ViewModel extends ContentStore {
  datamarts: IObservableArray<IDatamart>;

  constructor() {
    super();
    this.datamarts = observable.array([] as IDatamart[]);
    makeObservable(this);

    this.initialize();
  }

  private refreshIntervalId: number | null = null;

  private async initialize() {
    this.setStatus(StoreStatus.initializing);
    try {
      await this.refreshDatamarts();
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  public deregisterIntevals() {
    if (this.refreshIntervalId !== null)
      window.clearInterval(this.refreshIntervalId);
    this.refreshIntervalId = null;
  }

  public registerIntevals() {
    this.deregisterIntevals();
    this.refreshIntervalId = window.setInterval(
      this.refreshDatamarts.bind(this),
      3000
    );
  }

  private async refreshDatamarts() {
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
    const datamarts = (await response.json()) as IDatamart[];
    datamarts[0].status.state = DatamartStatus.failed;
    datamarts[1].status.state = DatamartStatus.running;

    this.setDatamarts(datamarts);
  }

  @action setDatamarts(newValue: IDatamart[]) {
    this.datamarts.replace(newValue);
  }

  // Upload Modal

  @observable isUploadDialogOpen: boolean = false;
  @action openUploadDialog() {
    this.isUploadDialogOpen = true;
    this.uploadName = "";
    this.setUploadType(DatamartType.csv);
  }
  @action closeUploadDialog() {
    this.isUploadDialogOpen = false;
    this.setUploadType(DatamartType.csv);
    this.uploadName = "";
  }

  @observable uploadName: string = "";
  @action setUploadName(value: string) {
    this.uploadName = value;
  }

  @observable bodyContentViewModel: BodyViewModel | null = null;
  @observable uploadType: DatamartType = DatamartType.csv;
  @action async setUploadType(value: DatamartType) {
    this.uploadType = value;
    await import("./body/" + this.uploadType).then((res) => {
      runInAction(() => {
        this.bodyContentViewModel = new res.default() as BodyViewModel;
      });
    });
  }

  @computed get bodyView() {
    if (!this.bodyContentViewModel) return null;
    return this.bodyContentViewModel.getView();
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
      formData.append("human_readable_name", this.uploadName);
      if (this.bodyContentViewModel) this.bodyContentViewModel.fill(formData);

      const configs = {
        method: "POST",
        headers: {
          Accept: "application/json",
        },
        body: formData,
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/datamarts/ingestion/${this.uploadType}`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      runInAction(async () => {
        this.datamarts.push((await response.json()) as IDatamart);
      });
      this.closeUploadDialog();
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @observable annotationViewModel: ContentStore | null = null;
  @action beginAnnotation(item: IDatamart) {
    this.annotationViewModel = new AnnotationViewModel(item);
  }
  @action endAnnotation() {
    this.annotationViewModel = null;
  }
  @computed get isAnnotationModalOpen() {
    return Boolean(this.annotationViewModel);
  }

  @computed get annotationView() {
    if (!this.annotationViewModel) return null;
    return this.annotationViewModel.getView();
  }

  async delete(item: IDatamart) {
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
        `/workspaces/${workspacesStore.currentWorkspace.id}/datamarts/${item.uid}`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      this.datamarts.remove(item);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
