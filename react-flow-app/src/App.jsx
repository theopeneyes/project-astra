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

// const fetchInitialNodes = async () => {
//   let response = await fetch(url).then((response) => response.json()); 
//   return response  
// }

// const dataset = await fetchInitialNodes()
// const initialNodes = dataset[0]; 
// const initialEdges = dataset[1]; 

// console.log(initialNodes, initialEdges); 
// const initialNodes = [
//   {
//     "id":"writing_a_c_compiler-20-70.pdf",
//     "position":{
//        "x":0,
//        "y":0
//     },
//     "data":{
//        "label":"writing_a_c_compiler-20-70.pdf"
//     }
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "position":{
//        "x":100,
//        "y":-100
//     },
//     "data":{
//        "label":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler"
//     }
//  },
//  {
//     "id":"Writing the Code Generator",
//     "position":{
//        "x":200,
//        "y":-200
//     },
//     "data":{
//        "label":"Writing the Code Generator"
//     }
//  }, 

//  {
//   "id":"Converting TACKY to Assembly",
//   "position":{
//      "x":200,
//      "y":-192
//   },
//   "data":{
//      "label":"Converting TACKY to Assembly"
//   }
// },
// {
//   "id":"Formatting assembly",
//   "position":{
//      "x":200,
//      "y":-184
//   },
//   "data":{
//      "label":"Formatting assembly"
//   }
// },
// {
//   "id":"Testing the Whole Compiler",
//   "position":{
//      "x":200,
//      "y":-176
//   },
//   "data":{
//      "label":"Testing the Whole Compiler"
//   }
// }

// ]


// const initialEdges = [
//   {
//     "id":"writing_a_c_compiler-20-70.pdf=Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "source":"writing_a_c_compiler-20-70.pdf",
//     "target":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler"
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler=Writing the Code Generator",
//     "source":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "target":"Writing the Code Generator"
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler=Converting TACKY to Assembly",
//     "source":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "target":"Converting TACKY to Assembly"
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler=Formatting assembly",
//     "source":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "target":"Formatting assembly"
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler=Testing the Whole Compiler",
//     "source":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "target":"Testing the Whole Compiler"
//  },
//  {
//     "id":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler=Implementation Tips",
//     "source":"Writing a C Compiler (Early Access) © 2022 by Nora Sandler",
//     "target":"Implementation Tips"
//  },
// ]

function App() {
  // add effect 
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]); // console.log(backendData)

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
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      />
    </div>
  );

}


export default App
