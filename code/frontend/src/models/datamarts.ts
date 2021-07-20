export enum DatamartType {
  csv = "csv",
  json = "json",
  xml = "xml",
  mongodb = "mongodb",
  postgres = "postgres",
}

export interface IDatamart {
  humanReadableName: string;
  uid: string;
  source: IDatamartStorage;
  target: IDatamartStorage;
  comment: string;
  status: IDatamartStatus;
  metadata: Metadata;
}

export interface Metadata {
  schema: Schema;
}

export interface Schema {
  fields: Field[];
}

export interface Field {
  name: string;
  nullable: boolean;
  type: FieldType;
}

export interface Struct {
  type: "struct";
  fields: Field[];
}

type FieldType = "string" | "integer" | "boolean" | "long" | Struct | Array;

export interface Array {
  type: "array";
  elementType: FieldType;
}

export function isStruct(item: FieldType): item is Struct {
  return typeof item === "object" && item !== null && item.type == "struct";
}

export function isArray(item: FieldType): item is Array {
  return typeof item === "object" && item !== null && item.type == "array";
}

export interface IDatamartStatus {
  state: DatamartStatus;
}

export enum DatamartStatus {
  success = "success",
  failed = "failed",
  running = "running",
}

export interface IDatamartStorage {
  datatype: DatamartType;
  uid: string;
  source: IDatamartStorage;
  comment: string;
  status: IDatamartStatus;
}

export interface Annotation {
  comment: string;
  data_attribute: string;
  datamart_id: string;
  ontology_attribute: [string, string][];
}
