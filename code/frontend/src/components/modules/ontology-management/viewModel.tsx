import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
  runInAction,
} from "mobx";
import React from "react";
import { render } from "react-dom";
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


export interface IData {
  Data: string;
}

class ViewModel extends ContentStore {
  ontologies: IObservableArray<IOntology>;

  constructor() {
    super();
    this.ontologies = observable.array([] as IOntology[]);
    this.Data = observable.array([] as IData[]);
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

  @action setOntologies(newValue: IOntology[])
  /**
   *
   * @param newValue
   */
  {
    this.ontologies.clear();
    this.ontologies.push(...newValue);
  }

  /* Sayeds Part Start */
  @observable QueryString: string = "";
  /**
   *
   * @param value
   */

  @action setQueryString(value: string) {
    this.QueryString = value;
  }

  @observable GraphName: string = "";
  /**
   *
   * @param value
   */
  @action setGraphName(value: string) {
    this.GraphName = value;
  }

  @observable IsQuery: boolean = true;
  /**
   *
   * @param value
   */
  @action setIsQuery(value: boolean) {
    this.IsQuery = value;
  }

  @observable Querysent: boolean = false;
  /**
   *
   * @param value
   */
  @action setQuerysent(value: boolean)
  /**
   *
   * @param value
   */
  {
    this.Querysent = value;
  }

  @action setData(newValue: IData[])
  /**
   *
   * @param newValue
   */
  {
    this.setData.clear();
    this.Data.push(...newValue);
  }

  async query() {

    this.setStatus(StoreStatus.working);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");
      const queryformData = new FormData();
      queryformData.append("Querystring", this.QueryString);
      queryformData.append("Graphname", this.GraphName);
      queryformData.append("Graphname", this.IsQuery);

      const configs = {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      };

      if (this.IsQuery == true) {
        var URI = `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/search?`
          + new URLSearchParams({
            querystring: this.QueryString.toString(),
            is_query: "True",
            graph_name: this.GraphName.toString(),
          })
      } else {
        var URI = `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/search?`
          + new URLSearchParams({
            querystring: this.QueryString.toString(),
            graph_name: this.GraphName.toString(),
          })
      }
      console.log("URI",URI)
      const response = await fetch(URI, configs);
      if (!response.ok) throw new Error(response.statusText);
      this.setStatus(StoreStatus.ready);
      this.Querysent = true;
      runInAction(async () => {
        this.Data.push((await response.json()) as IData);
      });
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }
  /* Sayeds Part End*/

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
  /**
   *
   * @param value
   */
  @action setUploadName(value: string)
  /**
   *
   * @param value
   */
  {
    this.uploadName = value;
  }

  @observable uploadFile: File | null = null;
  /**
   *
   * @param value
   */
  @action setUploadFile(value: File | null)
  /**
   *
   * @param value
   */
  {
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
