export enum DataSetType {
  csv = "csv",
}

export interface IDataSet {
  name: string;
  id: string;
  type: DataSetType;
}

export interface CsvDataSet extends IDataSet {
  type: DataSetType.csv;
  delimiter: string;
}
