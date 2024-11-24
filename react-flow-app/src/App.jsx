import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'; 
import React, { useCallback } from 'react';
import JsonSidebar from './components/JsonSidebar'; 

import "./App.css"
import "./index.css"

import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  Background, 
  BackgroundVariant, 
  addEdge,
} from '@xyflow/react';
 
import '@xyflow/react/dist/style.css';

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


function App() {

  const params = useParams(); 
  const emailId = params.emailId; 
  const fileName = params.fileName;  
  const url = `http://127.0.0.1:8000/reactFlow/${emailId}/${fileName}` 

  // add effect 
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]); // console.log(backendData)
  const [nodeName, setNodeName] = useState(params.fileName); 
  const [nodeType, setNodeType] = useState("Book"); 

  const onNodeClick = (_, node) => {
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
  }

  useEffect(() => {
    const fetchUrlData = async () => {
      await fetch(url).then(
        async (response) => await response.json()
      ).then(async (data) => {
        let [initialNodes, initialEdges] = data; 
        setNodes(initialNodes); 
        setEdges(initialEdges); 
      })
    }
    fetchUrlData(); 
  }, [])


  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  return (
    <ErrorBoundary> 
      <div className="Main">
        <div className="Reactflow">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
          >
            <Background variant={BackgroundVariant.Dots}></Background>
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


export default App
