import React, { useState, useEffect, useCallback, useRef } from "react";
import { Input, NumericTextBox } from "@progress/kendo-react-inputs";
import { DropDownList, MultiSelect } from "@progress/kendo-react-dropdowns";
import PerfectScrollbar from "perfect-scrollbar";
import { Button } from "@progress/kendo-react-buttons";
import '@xyflow/react/dist/style.css';
import "./xy-theme.css";
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  addEdge,
  MiniMap,
  Controls,
} from "@xyflow/react";

import ColorSelectorNode from "./ColorSelectorNode";

const topicWise = [
  "Topic 1",
  "Topic 2",
  "Topic 3",
  "Topic 4",
  "Topic 5",
  "Topic 6",
  "Topic 7",
  "Topic 8",
];
const multiSelect = [
  "Option 1",
  "Option 2",
  "Option 3",
  "Option 4",
  "Option 5",
  "Option 6",
  "Option 7",
  "Option 8",
];
const initBgColor = "#c9f1dd";

const snapGrid = [20, 20];
const nodeTypes = {
  selectorNode: ColorSelectorNode,
};

const defaultViewport = { x: 0, y: 0, zoom: 1.5 };
const ReactFlowPreview = () => {
  const reactflowScrollContainerRef = useRef(null);
  const psInstances = useRef({});
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [bgColor, setBgColor] = useState(initBgColor);

  useEffect(() => {
    if (reactflowScrollContainerRef.current) {
      psInstances.current.second = new PerfectScrollbar(
        reactflowScrollContainerRef.current
      );
    }

    // Initialize PerfectScrollbar for the "k-multiselect" dropdown
    const multiSelectElementContainer = document.querySelector(
      ".k-list-container .k-list-content"
    );
    if (multiSelectElementContainer) {
      psInstances.current.multiSelect = new PerfectScrollbar(
        multiSelectElementContainer
      );
    }
    const multiSelectElement = document.querySelector(".k-multiselect");
    if (multiSelectElement) {
      psInstances.current.multiSelect = new PerfectScrollbar(
        multiSelectElement
      );
    }

    // Cleanup on component unmount
    return () => {
      Object.values(psInstances.current).forEach((instance) => {
        if (instance) {
          instance.destroy();
        }
      });
      psInstances.current = {};
    };
  }, []);

  useEffect(() => {
    const onChange = (event) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id !== "2") {
            return node;
          }

          const color = event.target.value;

          setBgColor(color);

          return {
            ...node,
            data: {
              ...node.data,
              color,
            },
          };
        })
      );
    };

    setNodes([
      {
        id: "1",
        type: "input",
        data: { label: "An input node" },
        position: { x: 0, y: 100 },
        sourcePosition: "right",
      },
      {
        id: "2",
        type: "selectorNode",
        data: { onChange: onChange, color: initBgColor },
        position: { x: 300, y: 50 },
      },
      {
        id: "3",
        type: "output",
        data: { label: "Output A" },
        position: { x: 650, y: 25 },
        targetPosition: "left",
      },
      {
        id: "4",
        type: "output",
        data: { label: "Output B" },
        position: { x: 650, y: 100 },
        targetPosition: "left",
      },
    ]);

    setEdges([
      {
        id: "e1-2",
        source: "1",
        target: "2",
        animated: true,
      },
      {
        id: "e2a-3",
        source: "2",
        target: "3",
        sourceHandle: "a",
        animated: true,
      },
      {
        id: "e2b-4",
        source: "2",
        target: "4",
        sourceHandle: "b",
        animated: true,
      },
    ]);
  }, []);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, animated: true }, eds)),
    []
  );

  return (
    <>
      {/* First scrollable container */}
        <h2>Book Name</h2>
      <div className="default-box rf-preview p-0 border-0">
        <div className="rf-preview-inner" style={{ height: "calc(100vh - 219px)" }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            className="bg-transparent"
            nodeTypes={nodeTypes}
            snapToGrid={true}
            snapGrid={snapGrid}
            defaultViewport={defaultViewport}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
          </ReactFlow>
        </div>
      </div>

      {/* Second scrollable container */}
      <div ref={reactflowScrollContainerRef} className="reactflow-sidebar">
        <form>
          <div className="form-group">
            <label>Select the tree hierarchy</label>
            <DropDownList data={topicWise} defaultValue="Topic 1" />
          </div>
          <div className="form-group">
            <label className="w-100">True/False</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          {/* <div className="form-group">
            <label>File</label>
            <MultiSelect
              data={multiSelect}
              placeholder="Please select options"
            />
          </div> */}
          <div className="form-group">
            <label className="w-100">File in the blanks</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          <div className="form-group">
            <label className="w-100">Short Question Answer</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          <div className="form-group">
            <label className="w-100">Multiple Choose</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          <div className="form-group">
            <label className="w-100">Computational Questions</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          <div className="form-group">
            <label className="w-100">Software Code Questions</label>
            <NumericTextBox
              placeholder="Please enter value"
              defaultValue={0}
              format="n0"
            />
          </div>
          <div className="d-flex justify-content-center">
            <Button className="btn-design btn-2" type="submit">
              Push Changes
            </Button>
          </div>
        </form>
      </div>
    </>
  );
};

export default ReactFlowPreview;
