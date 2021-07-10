import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  aggregate: {};
}

export default {
  aggregate: {},
  schema: {
    fields: [],
  },
} as IData;
