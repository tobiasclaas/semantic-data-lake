import { action, computed, makeObservable, observable } from "mobx";
import React from "react";
import ContentStore from "../../../models/contentStore";
import StoreStatus from "../../../models/storeStatus.enum";
import appStore from "../../../stores/app.store";
import routingStore from "../../../stores/routing.store";
import View from "./main.component";

class ViewModel extends ContentStore {
  @observable username: string = "";
  @observable password: string = "";

  constructor() {
    super();
    appStore.setIsLoggedIn(false);
    makeObservable(this);
  }

  @action setUsername(value: string) {
    this.username = value;
  }

  @action setPassword(value: string) {
    this.password = value;
  }

  @computed get canLogin(): boolean {
    return this.password.length > 0 && this.username.length > 0;
  }

  async login() {
    this.setStatus(StoreStatus.initializing);
    try {
      const configs = {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: this.username,
          password: this.password,
        }),
      };
      const response = await fetch(`/auth/login`, configs);
      if (!response.ok) throw new Error(response.statusText);
      appStore.setIsLoggedIn(true);
      routingStore.history.push("/dashboard");
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
