import { NodeData } from "../../../../../models/workflow";

export interface IData extends NodeData {
  distinct: boolean;
}

export default {
  distinct: false,
  schema: {
    fields: [],
  },
} as IData;
