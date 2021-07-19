import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
   /**
   * @data export
   * @data type selection
   */
  name: string;
  target: string;
}

export default {
  name: "exported.csv",
  target: "HDFS",
} as IData;
