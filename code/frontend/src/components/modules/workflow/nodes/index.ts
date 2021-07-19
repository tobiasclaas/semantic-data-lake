import { DataSourceNode } from "./data_source";
import { JoinNode } from "./join";
import { ExportNode } from "./export";
import { FilterNode } from "./filter";
import { SelectNode } from "./select";
import { GroupbyNode } from "./groupby";
import { FlattenNode } from "./flatten";

export enum NodeType {
  data_source = "data_source",
  join = "join",
  export = "export",
  filter = "filter",
  select = "select",
  groupby = "groupby",
  flatten = "flatten",
}

const nodes: { [key in NodeType]: any } = {
  [NodeType.data_source]: DataSourceNode,
  [NodeType.join]: JoinNode,
  [NodeType.export]: ExportNode,
  [NodeType.filter]: FilterNode,
  [NodeType.select]: SelectNode,
  [NodeType.groupby]: GroupbyNode,
  [NodeType.flatten]: FlattenNode,
};

export default nodes;
