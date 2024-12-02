import React from 'react';
import { Handle, Position, useReactFlow } from '@xyflow/react';
import "./styles.module.css"; 


function CustomNode({ data, id, sourcePosition, targetPosition, positionAbsoluteX, positionAbsoluteY }) {
  const { addNodes, addEdges } = useReactFlow();

  const getLabel = ({ label, expanded, expandable }) => {
    if (!expandable) {
      return label;
    }
    return expanded ?  `${label} ▲` : `${label} ▼`;
  };

  const addChildNode = (evt) => {
    if (data.expanded) {
      evt.preventDefault();
      evt.stopPropagation();
    }

    const newNodeId = `${id}__${new Date().getTime()}`;

    addNodes({
      id: newNodeId,
      sourcePosition: sourcePosition, 
      targetPosition: targetPosition,  
      position: { x: positionAbsoluteX , y: positionAbsoluteY + 200 },
      data: { label: label },
    });
    addEdges({ id: `${id}->${newNodeId}`, source: id, target: newNodeId });
  };

  const label = getLabel(data);

  return (
    <div className="node">
      <div className="label">{label}</div>
      <Handle position={Position.Left} type="target" />
      <Handle position={Position.Right} type="source" />
      <div className="button" onClick={addChildNode} />
    </div>
  );
}

export default CustomNode;
