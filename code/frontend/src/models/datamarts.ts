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
  type: "string" | "integer" | Struct | Array;
}

export interface Struct {
  type: "struct";
  fields: Field[];
}

export interface Array {
  type: "array";
  elementType: ArrayElementType;
}

export interface ArrayElementType {
  fields: Field[];
}
export function isStruct(item: Struct | Array): item is Struct {
  return item.type == "struct";
}

export function isArray(item: Struct | Array): item is Array {
  return item.type == "array";
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
