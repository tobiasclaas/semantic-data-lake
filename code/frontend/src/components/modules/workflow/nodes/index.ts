import { DataSourceNode } from "./data_source";
import { JoinNode } from "./join";
import { ExportNode } from "./export";
import { FilterNode } from "./filter";
import { SelectNode } from "./select";
import { groupbyNode } from "./groupby";

export enum NodeType {
  data_source = "data_source",
  join = "join",
  export = "export",
  filter = "filter",
  select = "select",
  groupby = "groupby",
}

const nodes: { [key in NodeType]: any } = {
  [NodeType.data_source]: DataSourceNode,
  [NodeType.join]: JoinNode,
  [NodeType.export]: ExportNode,
  [NodeType.filter]: FilterNode,
  [NodeType.select]: SelectNode,
  [NodeType.groupby]: groupbyNode,
};

export default nodes;
