import { observable, action, makeObservable, IObservableArray } from "mobx";
import StoreStatus from "../models/storeStatus.enum";
import { IWorkspace, IWorkspaceExchange } from "../models/workspace";

class WorkspacesStore {
  @observable status: StoreStatus = StoreStatus.uninitialized;
  workspaces: IObservableArray<IWorkspace>;
  @observable currentWorkspace: IWorkspace | null = null;

  constructor() {
    this.workspaces = observable.array([] as IWorkspace[]);
    makeObservable(this);
    this.initialize();
  }

  private async initialize() {
    this.setStatus(StoreStatus.initializing);
    try {
      const configs = {
        method: "GET",
        headers: { Accept: "application/json" },
      };
      const response = await fetch("/workspaces", configs);
      if (!response.ok) throw new Error(response.statusText);
      const workspaces = (await response.json()) as IWorkspace[];
      this.setWorkspaces(workspaces);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action setStatus(newValue: StoreStatus) {
    this.status = newValue;
  }

  @action setWorkspaces(newValue: IWorkspace[]) {
    this.workspaces.clear();
    this.workspaces.push(...newValue);
    this.currentWorkspace = this.workspaces[0];
  }

  @action private addWorkspaceInternal(item: IWorkspace) {
    this.workspaces.push(item);
    this.currentWorkspace = item;
  }

  async addWorkspace(newValue: IWorkspaceExchange) {
    this.setStatus(StoreStatus.working);
    try {
      const configs = {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newValue),
      };
      const response = await fetch("/workspaces", configs);
      if (!response.ok) throw new Error(response.statusText);
      const workspace = (await response.json()) as IWorkspace;
      this.addWorkspaceInternal(workspace);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action setCurrentWorkspace(newValue: IWorkspace) {
    if (this.workspaces.indexOf(newValue) > -1)
      this.currentWorkspace = newValue;
  }

  @action private deleteWorkspaceInternal(item: IWorkspace) {
    this.workspaces.remove(item);
  }

  async deleteWorkspace(item: IWorkspace) {
    this.setStatus(StoreStatus.working);
    const id = item.id;
    try {
      const configs = {
        method: "DELETE",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id }),
      };
      const response = await fetch("/workspaces", configs);
      if (!response.ok) throw new Error(response.statusText);
      this.deleteWorkspaceInternal(item);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }
}

const workspacesStore = new WorkspacesStore();
export default workspacesStore;
