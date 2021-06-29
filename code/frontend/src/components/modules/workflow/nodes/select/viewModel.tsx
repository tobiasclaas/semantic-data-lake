import { action, computed, makeObservable, observable } from "mobx";
import React from "react";
import { IDatamart } from "../../../../../models/datamarts";
import { NodeData } from "../../../../../models/workflow";
import PropertiesViewModel from "../../propertiesViewModel";
import Dialog from "./dialog";
import WorkflowViewModel from "../..";
import { IData } from "./data";
import WorkflowHelper from "../../../../../utils/helpers/workflowHelper";

class ViewModel extends PropertiesViewModel<IData> {
  constructor(workflowViewModel: WorkflowViewModel, id: string, data: IData) {
    super(workflowViewModel, id, data);

    const node = workflowViewModel.getNode(id);
    if ((node.data?.schema.fields ?? []).length == 0) {
      const input = WorkflowHelper.getInputNodes(
        node,
        workflowViewModel.elements
      );
      if (input.length == 1)
        this.data.schema.fields = [
          ...(input[0].node.data?.schema.fields ?? []),
        ];
    }

    makeObservable(this);
  }

  getView() {
    return <Dialog viewModel={this} />;
  }

  @computed get currentFields() {
    const node = this.workflowViewModel.getNode(this.id);
    const inputs = WorkflowHelper.getInputNodes(
      node,
      this.workflowViewModel.elements
    );
    return (
      inputs.find((i) => i.name == "input")?.node?.data?.schema?.fields ?? []
    );
  }
}

export default ViewModel;
