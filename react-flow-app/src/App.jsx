import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'; 
import React, { useCallback } from 'react';
import JsonSidebar from './components/JsonSidebar'; 

import "./App.css"
import "./index.css"


import {
  ReactFlow,
  ReactFlowProvider, 
  Background, 
  BackgroundVariant, 
  addEdge,
  MiniMap,
  applyEdgeChanges, 
  applyNodeChanges
} from '@xyflow/react';


import CustomNode from './CustomNode';
import useAnimatedNodes from './useAnimatedNodes';
import useExpandCollapse from './useExpandCollapse';
import { useControls } from 'leva';
import { useFetchNodes } from './useFetchNodes';


import '@xyflow/react/dist/style.css';
import styles from './styles.module.css';


class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      errorInfo: null,
    };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error,
      errorInfo,
    });
  }

  render() {
    if (this.state.errorInfo) {
      return <>Some thing wrong</>;
    }
    return this.props.children;
  }
}

const nodeTypes = {
  custom: CustomNode,
};

function ReactFlowApp({
  treeWidth = 220,
  treeHeight = 100,
  animationDuration = 300,
}) {

  const params = useParams(); 
  const emailId = params.emailId; 
  const fileName = params.fileName;  
  const url = `http://127.0.0.1:8000/reactFlow/${emailId}/${fileName}` 
  const proOptions = { account: 'paid-pro', hideAttribution: true };
  const { initialNodes, initialEdges } = useFetchNodes(url); 
  
  // add effect 
  console.log("Initial Nodes", initialNodes); 
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges); // console.log(backendData)

  const [nodeName, setNodeName] = useState(params.fileName); 
  const [nodeType, setNodeType] = useState("Book"); 

  console.log("Nodes", nodes); 

  const { nodes: visibleNodes, edges: visibleEdges } = useExpandCollapse(
    nodes,
    edges,
    {treeWidth, treeHeight}
  );

  console.log("The visibleNodes vector = ", visibleNodes)

  const { nodes: animatedNodes } = useAnimatedNodes(visibleNodes, {
    animationDuration,
  });

  console.log(animatedNodes); 

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );


  const onNodeClick = useCallback(
      (_, node) => {
        setNodeName(node.data.label); 
        if(node.id.startsWith("chapter")) {
          setNodeType("Chapter"); 
        } else if (node.id.startsWith("topic")) {
          setNodeType("Topic"); 
        } else if(node.id.startsWith("sub_heading")) {
          setNodeType("Sub Heading"); 
        } else if (node.id.startsWith("text")) {
          setNodeType("Text")
        } else {
          setNodeType("Book")
        }

        setNodes((nds) =>
          nds.map((n) => {
            if (n.id === node.id) {
              return {
                ...n,
                data: { ...n.data, expanded: !n.data.expanded },
              };
            }

            return n;
          })
        );
      }, [setNodes]
  ); 

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <ErrorBoundary> 
      <div className="Main">
        <div className="Reactflow">
          <ReactFlow
            fitView 
            nodes={animatedNodes}
            edges={visibleEdges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodesDraggable={false}
            nodesConnectable={false}
            nodeTypes={nodeTypes}
            onNodeClick={onNodeClick}
            proOptions={proOptions}
            className={styles.viewport}
            zoomOnDoubleClick={false}
            elementsSelectable={false}
          >
            <Background variant={BackgroundVariant.Dots} />
            <MiniMap/> 
          </ReactFlow> 
        </div>
        <div className="Sidebar">
          <JsonSidebar 
            nodeName={nodeName} 
            nodeType={nodeType} 
          /> 
        </div>
      </div> 
    </ErrorBoundary>
  );

}

function App() {
  const levaProps = useControls({
    treeWidth: {
      value: 220,
      min: 0,
      max: 440,
    },
    treeHeight: {
      value: 100,
      min: 0,
      max: 200,
    },
    animationDuration: {
      value: 300,
      min: 0,
      max: 600,
    },
  });

  return (
    <>
    <ReactFlowProvider>
      <ReactFlowApp {...levaProps} /> 
    </ReactFlowProvider>
    </>
  )
  
}


export default App
