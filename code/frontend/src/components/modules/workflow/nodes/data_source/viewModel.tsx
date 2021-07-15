import { action, makeObservable, observable } from "mobx";
import React from "react";
import { IDatamart } from "../../../../../models/datamarts";
import { NodeData } from "../../../../../models/workflow";
import PropertiesViewModel from "../../propertiesViewModel";
import Dialog from "./dialog";
import WorkflowViewModel from "../..";
import { IData } from "./data";

class ViewModel extends PropertiesViewModel<IData> {
  constructor(workflowViewModel: WorkflowViewModel, id: string, data: IData) {
    super(workflowViewModel, id, data);
    makeObservable(this);
  }

  getView() {
    return <Dialog viewModel={this} />;
  }
}

export default ViewModel;