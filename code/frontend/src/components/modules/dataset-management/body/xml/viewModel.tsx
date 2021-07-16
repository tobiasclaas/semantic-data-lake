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
    formData.append("row_tag", this.Row_Tag);
    formData.append("root_tag", this.Root_Tag);
    formData.append("target_storage", this.target_storage);
    formData.append("comment", this.comment);

  }

  constructor() {
    /**
     * @Params Row_Tag, Root_Tag, Comment, Target_Storage.
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

  @observable Row_Tag: string = '';
  /**
   *
   * @param value
   */
  @action setRow_Tag(value: string) {
    this.Row_Tag = value;
  }

  @observable Root_Tag: string = '';
  /**
   *
   * @param value
   */
  @action setRoot_Tag(value: string) {
    this.Root_Tag = value;
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
