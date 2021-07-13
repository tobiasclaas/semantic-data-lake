import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  name: string;
  target: string;
}

export default {
  name: "exported.csv",
  target: "HDFS",
} as IData;
