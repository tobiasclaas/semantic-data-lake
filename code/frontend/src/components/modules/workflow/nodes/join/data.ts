import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  field: {
    input_1: string;
    input_2: string;
  };
}

export default {
  field: {
    input_1: "",
    input_2: "",
  },
  schema: {
    fields: [],
  },
} as IData;
