import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
  runInAction,
} from "mobx";
import React from "react";
import BodyViewModel from "../bodyViewModel";
import View from "./main.component";

class ViewModel extends BodyViewModel {
  fill(formData: FormData): void {
    formData.append("host", this.Host);
    formData.append("port", this.Port);
    formData.append("database", this.DataBase);
    formData.append("collection", this.Collection);
    formData.append("target_storage", this.Target_Storage);
    formData.append("user", this.User);
    formData.append("password", this.Password);
    formData.append("comment", this.Comment);
  }

  constructor() {
    super();
    makeObservable(this);
  }

  @observable Host: string = '';
  @action setHost(value: string) {
    this.Host = value;
  }

  @observable Port: string = '';
  @action setPort(value: string) {
    this.Port = value;
  }

  @observable DataBase: string = "";
  @action setDataBase(value: string) {
    this.DataBase = value;
  }

  @observable Collection: string = "";
  @action setCollection(value: string) {
    this.Collection = value;
  }

  @observable Target_Storage: string = "HDFS";
  @action setTarget_Storage(value: string) {
    this.Target_Storage = value;
  }

  @observable User: string = "";
  @action setUser(value: string) {
    this.User = value;
  }

  @observable Password: string = "";
  @action setPassword(value: string) {
    this.Password = value;
  }

  @observable Comment: string = "";
  @action setComment(value: string) {
    this.Comment = value;
  }

  canUpload(): boolean {
    return this.file !== null;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
