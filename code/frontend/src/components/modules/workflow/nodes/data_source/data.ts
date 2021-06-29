import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  uid: string;
}

export default {
  uid: "",
  schema: {
    fields: [],
  },
} as IData;
