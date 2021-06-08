import React, { useRef, useState } from "react";
import { observer } from "mobx-react-lite";
import ViewModel from "./viewModel";
import IViewProps from "../../../models/iViewProps";
import { useTranslation } from "react-i18next";
import workspacesStore from "../../../stores/workspaces.store";
import Sidebar from "./sidebar";
import { useLocalObservable } from "mobx-react-lite";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls,
  OnLoadParams,
  Connection,
  Edge,
  FlowElement,
  Node as FlowNode,
  Elements,
  XYPosition,
} from "react-flow-renderer";
import { v4 as uuidv4 } from "uuid";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [elements, setElements] = useState<Elements<any>>([]);

  const onConnect = (params: Edge<any> | Connection) =>
    setElements((els) => addEdge(params, els));

  const onElementsRemove = (elementsToRemove: Elements<any>) =>
    setElements((els) => removeElements(elementsToRemove, els));

  const onLoad = (_reactFlowInstance: OnLoadParams<any>) =>
    setReactFlowInstance(_reactFlowInstance);

  const generateNode = (type: string, position: XYPosition) => {
    let node: FlowNode<any> = {
      id: uuidv4(),
      position,
      data: { label: `${type} node` },
    };

    if (indexOf)
    return node;
  };

  const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (!reactFlowWrapper.current) return;
    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData("application/reactflow");
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });

    setElements((es) => es.concat(generateNode(type, position)));
  };

  return (
    <div style={{ flex: 1, display: "flex" }}>
      <ReactFlowProvider>
        <Sidebar viewModel={viewModel} />
        <div style={{ flex: 1 }} ref={reactFlowWrapper}>
          <ReactFlow
            elements={elements}
            onConnect={onConnect}
            onElementsRemove={onElementsRemove}
            onLoad={onLoad}
            onDrop={onDrop}
            onDragOver={onDragOver}
          >
            <Controls />
          </ReactFlow>
        </div>
      </ReactFlowProvider>
    </div>
  );
});

export default Main;
