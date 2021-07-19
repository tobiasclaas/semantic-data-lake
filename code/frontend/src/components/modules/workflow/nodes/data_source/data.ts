import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  /**
   * @data export
   * @data type selection
   */
  uid: string;
}

export default {
  uid: "",
  schema: {
    fields: [],
  },
} as IData;
