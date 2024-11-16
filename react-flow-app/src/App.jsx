import { useState, useEffect } from 'react'
import React, { useCallback } from 'react';
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react';
 
import '@xyflow/react/dist/style.css';



const emailId = "test.14@gmail.com" 
const fileName = "writing_a_c_compiler-20-70.pdf"
const url = `http://127.0.0.1:8000/reactFlow/${emailId}/${fileName}` 


function App() {
  const [backendData, setBackendData] = useState([[], []])
  // add effect 
  useEffect(() => {
    fetch(url).then(
      (response) => response.json()
    ).then(
      (data) => setBackendData(data))
  }, [])


  const initialNodes = [
    { id: 'anam malik', position: { x: 0, y: 0 }, data: { label: 'Node 1' } },
    { id: 'genie dashina', position: { x: 100, y: -100 }, data: { label: 'node 2' } },
    { id: 'fari fari', position: { x: -100, y: 100 }, data: { label: 'node 3' } },
  ];

  const initialEdges = [
    { id: 'e1-2', source: 'anam malik', target: 'fari fari', animated: true }, 
    { id:'e2-1', source: 'genie dashina', target:'fari fari', animated: true}
  ];

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges); // console.log(backendData)

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
       <ReactFlow
        nodes={nodes}
        edges={edges}
      />
    </div>
  );
}


export default App
