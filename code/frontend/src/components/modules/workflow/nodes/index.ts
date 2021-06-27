import DataSourceNode from "./data_source";
import JoinNode from "./join";
import ExportNode from "./export";

export enum NodeType {
  data_source = "data_source",
  join = "join",
  export = "export",
}

const nodes: { [key in NodeType]: any } = {
  [NodeType.data_source]: DataSourceNode,
  [NodeType.join]: JoinNode,
  [NodeType.export]: ExportNode,
};

export default nodes;
