import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  condition: string;
}

export default {
  condition: "",
  schema: {
    fields: [],
  },
} as IData;
