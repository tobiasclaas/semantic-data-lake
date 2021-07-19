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
    if (this.file) formData.append("file", this.file);
    formData.append("delimiter", this.delimiter);
    formData.append("has_header", this.hasHeader ? "1" : "0");
    formData.append("comment", this.comment);
    formData.append("target_storage", this.target_storage);
  }

  constructor() {
    /**
     * Param Delimiter, HasHeader, Comment, Target Storage.
     */
    super();
    makeObservable(this);
  }

  @observable file: File | null = null;
  /**
   *
   * @param value
   */
  @action setFile(value: File | null) {
    this.file = value;
  }

  @observable delimiter: string = ",";
  /**
   *
   * @param value
   */
  @action setDelimiter(value: string) {
    this.delimiter = value;
  }

  @observable hasHeader: boolean = true;
  /**
   *
   * @param value
   */
  @action setHasHeader(value: boolean) {
    this.hasHeader = value;
  }

  @observable target_storage: string = 'HDFS';
  /**
   *
   * @param value
   */
  @action setTargetStorage(value: string) {
    this.target_storage = value;
  }

  @observable comment: string = "";
  /**
   *
   * @param value
   */
  @action setComment(value: string) {
    this.comment = value;
  }

  canUpload(): boolean {
     /**
     * send upload request
     */
    return this.file !== null;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
