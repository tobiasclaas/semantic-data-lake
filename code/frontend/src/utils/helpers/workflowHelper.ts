import { toJS } from "mobx";
import { Elements, Node, Edge } from "react-flow-renderer";
import { NodeType } from "../../components/modules/workflow/nodes";
import { IData as DataSourceData } from "../../components/modules/workflow/nodes/data_source/data";
import { IData as ExportData } from "../../components/modules/workflow/nodes/export/data";
import { IData as JoinData } from "../../components/modules/workflow/nodes/join/data";
import { IData as FilterData } from "../../components/modules/workflow/nodes/filter/data";
import { IData as SelectData } from "../../components/modules/workflow/nodes/select/data";

import { NodeData } from "../../models/workflow";

interface InputDescription<T extends NodeData> {
  node: Node<T>;
  name: string;
}

abstract class WorkflowHelper {
  public static parseElements(elements: Elements<NodeData>): any {
    const exportNodes = elements.filter(
      (e) => e.type === NodeType.export
    ) as Node<any>[];
    return exportNodes.map((n) => WorkflowHelper.processNode(n, elements));
  }

  private static processNode(
    node: Node<NodeData>,
    elements: Elements<NodeData>
  ) {
    const data: any = {};
    data.type = node.type;

    switch (node.type) {
      case NodeType.data_source: {
        const nodeData = node.data as DataSourceData;
        data.uid = nodeData.uid;
        break;
      }

      case NodeType.filter: {
        const nodeData = node.data as FilterData;
        data.condition = nodeData.condition;
        data.input = WorkflowHelper.getInputNodes(node, elements).map((n) =>
          WorkflowHelper.processNode(n.node, elements)
        );
        break;
      }

      case NodeType.select: {
        const nodeData = node.data as SelectData;
        data.columns = nodeData.schema.fields.map((f) => f.name);
        data.input = WorkflowHelper.getInputNodes(node, elements).map((n) =>
          WorkflowHelper.processNode(n.node, elements)
        );
        break;
      }

      case NodeType.export: {
        const nodeData = node.data as ExportData;
        data.name = nodeData.name;
        data.target = nodeData.target;
        data.input = WorkflowHelper.getInputNodes(node, elements).map((n) =>
          WorkflowHelper.processNode(n.node, elements)
        );
        break;
      }

      case NodeType.join: {
        const nodeData = node.data as JoinData;
        data.input = WorkflowHelper.getInputNodes(node, elements).map((n) => ({
          input: [WorkflowHelper.processNode(n.node, elements)],
          column: (nodeData.field as any)[n.name],
        }));
        break;
      }
    }
    return data;
  }

  public static getInputNodes(
    node: Node<NodeData>,
    elements: Elements<NodeData>
  ) {
    const directedEdges = elements.filter(
      (e) => !e.type && (e as Edge<NodeData>).target === node.id
    ) as Edge<NodeData>[];

    return directedEdges.map(
      (e) =>
        ({
          name: e.targetHandle,
          node: elements.find((n) => n.id == e.source),
        } as InputDescription<NodeData>)
    );
  }
}

export default WorkflowHelper;
