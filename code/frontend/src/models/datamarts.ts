export enum DatamartType {
  csv = "csv",
  json = "json",
}

export interface IDatamart {
  humanReadableName: string;
  uid: string;
  source: IDatamartStorage;
  target: IDatamartStorage;
  comment: string;
  status: IDatamartStatus;
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
