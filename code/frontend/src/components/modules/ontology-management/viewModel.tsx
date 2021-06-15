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
  IOntology,
  IOntologyExchange,
  IOntologyPost,
} from "../../../models/ontology";
import StoreStatus from "../../../models/storeStatus.enum";
import routingStore from "../../../stores/routing.store";
import workspacesStore from "../../../stores/workspaces.store";
import View from "./main.component";

class ViewModel extends ContentStore {
  ontologies: IObservableArray<IOntology>;

  constructor() {
    super();
    this.ontologies = observable.array([] as IOntology[]);
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
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      const ontologies = await response.json();
      this.setOntologies(ontologies);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action setOntologies(newValue: IOntology[]) {
    this.ontologies.clear();
    this.ontologies.push(...newValue);
  }

  // Upload Modal

  @observable isUploadDialogOpen: boolean = false;
  @action openUploadDialog() {
    this.isUploadDialogOpen = true;
  }
  @action closeUploadDialog() {
    this.isUploadDialogOpen = false;
    this.uploadName = "";
  }

  @observable uploadName: string = "";
  @action setUploadName(value: string) {
    this.uploadName = value;
  }

  @observable uploadFile: File | null = null;
  @action setUploadFile(value: File | null) {
    this.uploadFile = value;
  }

  @computed get canUpload(): boolean {
    return this.uploadName.length > 0 && this.uploadFile !== null;
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
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      runInAction(async () => {
        this.ontologies.push((await response.json()) as IOntology);
      });
      this.closeUploadDialog();
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  async delete(item: IOntology) {
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
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/${item.id}`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      this.ontologies.remove(item);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;