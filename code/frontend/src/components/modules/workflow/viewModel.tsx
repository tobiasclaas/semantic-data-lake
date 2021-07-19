import { extendObservable, IObservableArray, runInAction, toJS } from "mobx";
import { action, makeObservable, observable } from "mobx";
import React from "react";
import ContentStore from "../../../models/contentStore";
import { DatamartStatus, IDatamart } from "../../../models/datamarts";
import StoreStatus from "../../../models/storeStatus.enum";
import appStore from "../../../stores/app.store";
import View from "./main.component";
import workspacesStore from "../../../stores/workspaces.store";
import { NodeData } from "../../../models/workflow";
import {
  addEdge as addEdgeRF,
  ArrowHeadType,
  Connection,
  Edge,
  Elements,
  FlowElement,
  isEdge,
  Node,
} from "react-flow-renderer";
import { v4 as uuidv4 } from "uuid";
import { computed } from "mobx";
import PropertiesViewModel from "./propertiesViewModel";
import { NodeType } from "./nodes";
import WorkflowHelper from "../../../utils/helpers/workflowHelper";

class ViewModel extends ContentStore {
  constructor() {
    super();
    this.isFullscreen = true;
    this.datamarts = observable.array([] as IDatamart[]);
    this.elements = observable.array([] as Elements<NodeData>);

    makeObservable(this);
    this.initialize();
  }

  @action addEdge(edgeParams: Edge<NodeData> | Connection) {
    let edge: Edge;
    edge = {
      ...edgeParams,
      id: uuidv4(),
      arrowHeadType: ArrowHeadType.Arrow,
    } as Edge;

    const connectionExists = this.elements.some(
      (el) =>
        isEdge(el) &&
        el.source === edge.source &&
        el.target === edge.target &&
        (el.sourceHandle === edge.sourceHandle ||
          (!el.sourceHandle && !edge.sourceHandle)) &&
        (el.targetHandle === edge.targetHandle ||
          (!el.targetHandle && !edge.targetHandle))
    );

    if (connectionExists) return;
    this.elements.push(edge as Edge);
  }

  @action removeElements(elementsToRemove: Elements<NodeData>) {
    elementsToRemove.map((e) => this.elements.remove(e));
  }

  @action deleteNode(id: string) {
    const elements = this.elements.filter(
      (e) => e.id === id || (isEdge(e) && (e.target === id || e.source === id))
    );
    if (elements.length === 0) return;
    elements.forEach((e) => this.elements.remove(e));
  }

  getNode(id: string) {
    const node = this.elements.find((e) => e.id === id) as Node<NodeData>;
    return node;
  }

  async addNode(type: NodeType, position: any) {
    await import(`./nodes/${type}/data`).then((data) => {
      let node: Node<NodeData> = {
        id: uuidv4(),
        position,
        data: data.default as NodeData,
        type,
      };
      runInAction(() => {
        this.elements.push(node);
      });
    });
  }

  datamarts: IObservableArray<IDatamart>;
  elements: IObservableArray<FlowElement<NodeData>>;

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
    this.setDatamarts(
      datamarts.filter((i) => i.status.state === DatamartStatus.success)
    );
  }

  @action setDatamarts(newValue: IDatamart[]) {
    this.datamarts.replace(newValue);
  }

  getView = () => <View viewModel={this} />;

  onDragStart = (event: React.DragEvent<HTMLElement>, nodeType: string) => {
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.effectAllowed = "move";
  };

  async submit() {
    if (!workspacesStore.currentWorkspace)
      throw new Error("Current workspace must be set.");

    this.setStatus(StoreStatus.working);
    try {
      const configs = {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(WorkflowHelper.parseElements(this.elements)),
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/workflow`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  /**
   * Properties
   */
  @observable propertiesViewModel: PropertiesViewModel<NodeData> | null = null;

  @computed get isPropertiesModalOpen() {
    return Boolean(this.propertiesViewModel);
  }

  async openPropertiesModal(node: Node<NodeData>) {
    if (node.type)
      await import(`./nodes/${node.type}`).then((res) => {
        runInAction(() => {
          this.propertiesViewModel = new res.default(
            this,
            node.id,
            node.data ? toJS(node.data) : {}
          ) as PropertiesViewModel<NodeData>;
        });
      });
  }

  @action closePropertiesModal() {
    this.propertiesViewModel = null;
  }

  @computed get propertiesModalContentView() {
    if (!this.propertiesViewModel) return null;
    return this.propertiesViewModel.getView();
  }

  @action saveProperties() {
    const viewModel = this.propertiesViewModel;
    if (!viewModel) return;
    const node = this.elements.find((e) => e.id === viewModel.id);
    if (node) {
      this.elements.remove(node);
      node.data = viewModel.data;
      this.elements.push(node);
    }
    this.closePropertiesModal();
  }
}

export default ViewModel;
