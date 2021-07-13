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
  data: IObservableArray<object>;
  headers: IObservableArray<object>;

  constructor(item: IDatamart) {
    super();
    this.data = observable.array([]);
    this.headers = observable.array([]);
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
        `/workspaces/${workspacesStore.currentWorkspace.id}/datamarts?uid=`+ item.uid +`&data_only=True`,
        configs
      ).then(res => res.json())
          .then(
              (result) => {
                const data = JSON.parse(result);
                const headers = Object.keys(data);
                // @ts-ignore
                  Object.keys(data).map((item) => this.headers.push(item));

                for (const [key, value] of Object.entries(data[headers[0]])) {
                    var row = new Array();
                    headers.forEach(function (item, index) {
                        row.push(data[item][key]);
                    });
                    this.data.push(row);
                }
              },
              (error) => {
                throw new Error(error.statusText);
              }
          )

      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      console.log(ex);
    }
  }


  getView = () => <View viewModel={this} />;
}

export default ViewModel;
