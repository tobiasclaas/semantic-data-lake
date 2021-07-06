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
    if (this.file) formData.append("file", this.file);
    formData.append("delimiter", this.delimiter);
    formData.append("has_header", this.hasHeader ? "1" : "0");
  }

  constructor() {
    super();
    makeObservable(this);
  }

  @observable file: File | null = null;
  @action setFile(value: File | null) {
    this.file = value;
  }

  @observable Row_Tag: string = '';
  @action setRow_Tag(value: string) {
    this.target_storage = value;
  }

  @observable target_storage: string = 'HDFS';
  @action setTargetStorage(value: string) {
    this.target_storage = value;
  }

  @observable comment: string = "";
  @action setComment(value: string) {
    this.comment = value;
  }

  canUpload(): boolean {
    return this.file !== null;
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
