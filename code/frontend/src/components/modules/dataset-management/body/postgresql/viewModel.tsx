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
  /**
   *
   * @param formData
   */
  fill(formData: FormData): void {
    formData.append("host", this.Host);
    formData.append("port", this.Port);
    formData.append("database", this.DataBase);
    formData.append("table", this.Table);
    formData.append("target_storage", "PostgreSQL");
    formData.append("user", this.User);
    formData.append("password", this.Password);
    formData.append("comment", this.Comment);
  }

  constructor() {
    /**
     * Param type string
     * Param Host, Port, DataBase, Table, Target_Storage, User, Password, Comment
     */
    super();
    makeObservable(this);
  }

  @observable Host: string = '';
  /**
   *
   * @param value
   */
  @action setHost(value: string) {
    this.Host = value;
  }

  @observable Port: string = '';
  /**
   *
   * @param value
   */
  @action setPort(value: string) {
    this.Port = value;
  }

  @observable DataBase: string = "";
  /**
   *
   * @param value
   */
  @action setDataBase(value: string) {
    this.DataBase = value;
  }

  @observable Table: string = "";
  /**
   *
   * @param value
   */
  @action setTable(value: string) {
    this.Table = value;
  }

  @observable Target_Storage: string = "PostgreSQL";
  /**
   *
   * @param value
   */
  @action setTarget_Storage(value: string) {
    this.Target_Storage = value;
  }

  @observable User: string = "";
  /**
   *
   * @param value
   */
  @action setUser(value: string) {
    this.User = value;
  }

  @observable Password: string = "";
  /**
   *
   * @param value
   */
  @action setPassword(value: string) {
    this.Password = value;
  }

  @observable Comment: string = "";
  /**
   *
   * @param value
   */
  @action setComment(value: string) {
    this.Comment = value;
  }

  canUpload(): boolean {
    /**
     * send upload request
     */
    return this.host !== null;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
