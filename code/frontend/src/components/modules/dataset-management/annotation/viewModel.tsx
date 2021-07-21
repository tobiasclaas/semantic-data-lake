import {
  action,
  computed,
  IObservableArray,
  makeObservable,
  observable,
} from "mobx";
import React from "react";
import ContentStore from "../../../../models/contentStore";
import { Annotation, Field, IDatamart } from "../../../../models/datamarts";
import StoreStatus from "../../../../models/storeStatus.enum";
import workspacesStore from "../../../../stores/workspaces.store";
import View from "./main.component";
import FieldView from "./fieldView.component";
import { AutocompleteItem } from "../../../../models/autocomplete";

class ViewModel extends ContentStore {
  @observable datamart: IDatamart | null = null;
  @observable field: Field | null = null;
  @observable path: string = "";
  annotations: IObservableArray<Annotation>;

  @observable annotationPropertyDescription: string = "";
  @observable annotationOntologyProperty: AutocompleteItem | null = null;

  constructor(item: IDatamart) {
    super();
    this.datamart = item;
    this.annotations = observable.array([] as Annotation[]);
    makeObservable(this);

    this.initialize();
  }

  @action setAnnotationPropertyDescription(newValue: string) {
    this.annotationPropertyDescription = newValue;
  }

  @action setAnnotationOntologyProperty(newValue: AutocompleteItem | null) {
    this.annotationOntologyProperty = newValue;
  }

  @action display(field: Field | null, path: string) {
    this.field = field;
    this.path = path;
    this.setAnnotationOntologyProperty(null);
    this.setAnnotationPropertyDescription("");
  }

  @computed get getFieldView() {
    return this.field ? (
      <FieldView viewModel={this} path={this.path} field={this.field} />
    ) : null;
  }

  @computed get canAddAnnotation() {
    return this.annotationOntologyProperty != null;
  }

  private async initialize() {
    if (!this.datamart) return;
    this.setStatus(StoreStatus.initializing);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const configs = {
        method: "GET",
        headers: { Accept: "application/json" },
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/annotation?datamart_id=${this.datamart.uid}`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      const annotations = (await response.json()) as Annotation[];
      this.setAnnotations(annotations);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  async deleteAnnotation(data_attribute: string, ontology_attribute: string) {
    if (!this.datamart) return;
    this.setStatus(StoreStatus.working);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const formData = new FormData();
      formData.append("datamart_id", this.datamart.uid);
      formData.append("data_attribute", data_attribute);
      formData.append("ontology_attribute", ontology_attribute);

      const configs = {
        method: "DELETE",
        headers: { Accept: "application/json" },
        body: formData,
      };
      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/annotation`,
        configs
      );
      if (!response.ok) throw new Error(response.statusText);
      this.deleteAnnotationInternal(data_attribute, ontology_attribute);
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  async addAnnotation() {
    if (!this.datamart) return;
    this.setStatus(StoreStatus.working);
    try {
      if (!workspacesStore.currentWorkspace)
        throw new Error("Current workspace must be set.");

      const formData = new FormData();
      formData.append("datamart_id", this.datamart.uid);
      formData.append("data_attribute", this.path);
      formData.append(
        "property_description",
        this.annotationPropertyDescription
      );
      if (this.annotationOntologyProperty)
        formData.append(
          "ontology_attribute",
          this.annotationOntologyProperty.value
        );

      const configs = {
        method: "POST",
        headers: { Accept: "application/json" },
        body: formData,
      };

      const response = await fetch(
        `/workspaces/${workspacesStore.currentWorkspace.id}/ontologies/annotation`,
        configs
      );

      if (!response.ok) throw new Error(response.statusText);
      this.initialize();
      this.setAnnotationOntologyProperty(null);
      this.setAnnotationPropertyDescription("");
      this.setStatus(StoreStatus.ready);
    } catch (ex) {
      this.setStatus(StoreStatus.failed);
    }
  }

  @action deleteAnnotationInternal(
    data_attribute: string,
    ontology_attribute: string
  ) {
    const attribute = this.annotations.find(
      (i) => i.data_attribute == data_attribute
    );
    if (!attribute) return;
    attribute.ontology_attribute = attribute.ontology_attribute.filter(
      (x) => x[1] !== ontology_attribute
    );
  }

  @action setAnnotations(newValue: Annotation[]) {
    this.annotations.clear();
    this.annotations.push(...newValue);
  }

  getView = () => <View viewModel={this} />;
}

export default ViewModel;
