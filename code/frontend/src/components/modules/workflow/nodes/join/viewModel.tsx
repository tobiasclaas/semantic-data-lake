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
  /**
   *
   * @param workflowViewModel
   * @param id
   * @param data
   */
  constructor(workflowViewModel: WorkflowViewModel, id: string, data: IData) {
    super(workflowViewModel, id, data);
    makeObservable(this);
  }

  getView() {
    return <Dialog viewModel={this} />;
  }

  @computed get firstInputFields() {
    /**
     * join workflowViewModel
     */
    const node = this.workflowViewModel.getNode(this.id);
    const inputs = WorkflowHelper.getInputNodes(
      node,
      this.workflowViewModel.elements
    );
    return (
      inputs.find((i) => i.name == "input_1")?.node?.data?.schema?.fields ?? []
    );
  }

  @computed get secondInputFields() {
    const node = this.workflowViewModel.getNode(this.id);
    const inputs = WorkflowHelper.getInputNodes(
      node,
      this.workflowViewModel.elements
    );
    return (
        /**
         * @return NodeData
         */
      inputs.find((i) => i.name == "input_2")?.node?.data?.schema?.fields ?? []
    );
  }
}

export default ViewModel;
