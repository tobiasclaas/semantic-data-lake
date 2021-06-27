import { Elements, Node, Edge } from "react-flow-renderer";
import { NodeType } from "../../components/modules/workflow/nodes";

abstract class WorkflowHelper {
  public static parseElements(elements: Elements<any>): any {
    const exportNodes = elements.filter(
      (e) => e.type === NodeType.export
    ) as Node<any>[];
    return exportNodes.map((n) => WorkflowHelper.processNode(n, elements));
  }

  private static processNode(node: Node<any>, elements: Elements<any>) {
    const data: any = {};
    data.type = node.type;
    Object.assign(data, node.data);

    switch (node.type) {
      case NodeType.export: {
        data.inputs = WorkflowHelper.getInputNodes(node, elements).map((n) =>
          WorkflowHelper.processNode(n, elements)
        );
        break;
      }
      case NodeType.join: {
        data.inputs = WorkflowHelper.getInputNodes(node, elements).map((n) =>
          WorkflowHelper.processNode(n, elements)
        );
        break;
      }
    }
    return data;
  }

  private static getInputNodes(node: Node<any>, elements: Elements<any>) {
    const directedEdges = elements.filter(
      (e) => !e.type && (e as Edge<any>).target === node.id
    ) as Edge<any>[];
    return directedEdges.map((e) =>
      elements.find((n) => n.id == e.source)
    ) as Node<any>[];
  }
}

export default WorkflowHelper;
