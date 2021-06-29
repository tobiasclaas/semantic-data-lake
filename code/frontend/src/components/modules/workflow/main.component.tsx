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
  ArrowHeadType,
} from "react-flow-renderer";
import { v4 as uuidv4 } from "uuid";
import nodes, { NodeType } from "./nodes";
import Button from "@material-ui/core/Button";
import WorkflowHelper from "../../../utils/helpers/workflowHelper";
import { NodeData } from "../../../models/workflow";
import { toJS } from "mobx";
import PropertiesDialog from "./propertiesDialog";

const Main: React.FC<IViewProps<ViewModel>> = observer(({ viewModel }) => {
  const reactFlowWrapper = useRef<HTMLDivElement | null>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);

  const onLoad = (_reactFlowInstance: OnLoadParams<any>) =>
    setReactFlowInstance(_reactFlowInstance);

  const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (!reactFlowWrapper.current) return;
    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData(
      "application/reactflow"
    ) as NodeType;
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    });

    viewModel.addNode(type, position);
  };

  return (
    <React.Fragment>
      <div style={{ flex: 1, display: "flex" }}>
        <ReactFlowProvider>
          <Sidebar viewModel={viewModel} />
          <div style={{ flex: 1 }} ref={reactFlowWrapper}>
            <ReactFlow
              elements={viewModel.elements.slice()}
              nodeTypes={nodes}
              onElementsRemove={(e) => viewModel.removeElements(e)}
              onConnect={(e) => viewModel.addEdge(e)}
              onLoad={onLoad}
              onNodeContextMenu={(e, node) => {
                e.preventDefault();
                viewModel.openPropertiesModal(node);
              }}
              onDrop={onDrop}
              onDragOver={onDragOver}
            >
              <Controls />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
      </div>
      <PropertiesDialog viewModel={viewModel} />
      <Button
        onClick={() => {
          console.log(
            toJS(WorkflowHelper.parseElements(viewModel.elements.slice()))
          );
        }}
      >
        Show Code
      </Button>
    </React.Fragment>
  );
});

export default Main;
