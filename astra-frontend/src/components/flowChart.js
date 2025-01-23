import React, { useState } from 'react';
import ReactFlow, { MiniMap, Controls } from 'react-flow-renderer';

const FlowChart = () => {
  const [nodes, setNodes] = useState([
    { id: '1', data: { label: 'Node 1' }, position: { x: 100, y: 100 } },
    { id: '2', data: { label: 'Node 2' }, position: { x: 300, y: 100 } },
  ]);

  const [edges, setEdges] = useState([{ id: 'e1-2', source: '1', target: '2', animated: true }]);

  const addNode = () => {
    const newNode = {
      id: `${nodes.length + 1}`,
      data: { label: `Node ${nodes.length + 1}` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
    };
    setNodes((prevNodes) => [...prevNodes, newNode]);
  };

  return (
    <div style={{ height: '100vh' }}>
      <button onClick={addNode}>Add Node</button>
      <ReactFlow nodes={nodes} edges={edges} style={{ background: '#f1f1f1' }}>
        <MiniMap />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default FlowChart;
