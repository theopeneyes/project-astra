import React from 'react'
import "../index.css"
import ChapterForm from './ChapterForm'
import {TopicForm} from './TopicForm'
import SidebarHeader from './SidebarHeader'
import SidebarTemplate from './SidebarTemplate'
import PropTypes from 'prop-types'
import BookForm from "./BookForm"
import HierarchyForm from './HierarchyForm'
import { useParams } from 'react-router-dom'


const JsonSidebar = (props) => {

  const params = useParams(); 
  const fileName = params.fileName; 
  const emailId = params.emailId; 

  const handlePush = async () => {
    let bookContent = [];  
    let chapterContent = []; 
    let topicContent = []; 

    for(let i = 0; i < localStorage.length; i++) {
      if(localStorage.key(i).startsWith("book")) {
        // need to also check if we are using the correct book 
        bookContent.push(JSON.parse(localStorage
          .getItem(localStorage.key(i)))); 

      }else if (localStorage.key(i).startsWith("chapter")) {
        chapterContent.push(JSON.parse(localStorage
          .getItem(localStorage.key(i)))); 

      } else if (localStorage.key(i).startsWith("topic")) {
        topicContent.push(JSON.parse(localStorage
          .getItem(localStorage.key(i))
        )); 
      }
    }

    try {
      const response = await fetch("http://localhost:8000/generation_data",{
        method: "POST", 
        headers: {
          'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
          emailId: emailId, 
          fileName: fileName, 
          category: (document
                    .getElementById("select-box-hierarchy")
                    .value
                    .split("-")
                    .at(0)), 
          generationData: {
            book: bookContent, 
            chapters: chapterContent, 
            topics: topicContent, 
          },  
        })
      })

      if(!response.ok) {
        throw new Error("Exception occured. Network didn't work."); 
      } else {
        // localStorage.clear(); 
      }

      console.log(response.json())
    } catch (error) {
      console.log(error); 
    }

  }

  if (props.nodeType == "Book") {
    return (
      <>
      <SidebarTemplate> 
        <div className="mb-5">
          <SidebarHeader ElementType="node_text" ElementValue={props.nodeName} /> 
          <SidebarHeader ElementType="node_type" ElementValue={props.nodeType} /> 
        </div>
        <div className="mb-5">
          <HierarchyForm updateNodes={props.updateNodesAndEdges} emailId={emailId} bookName={fileName}  />
        </div>
        <BookForm nodeId={props.nodeId} bookName={props.nodeName} />
        <div className="mt-auto">
          <button 
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
            onClick={handlePush}
          >
            Push Changes 
          </button>
        </div>
      </SidebarTemplate>
      </>
    )
  }
  else if(props.nodeType == "Chapter") {
    return (
      <>
      <SidebarTemplate> 
        <div className="mb-5">
          <SidebarHeader ElementType="node_text" ElementValue={props.nodeName} /> 
          <SidebarHeader ElementType="node_type" ElementValue={props.nodeType} /> 
        </div>
        <div className="mb-5">
          <HierarchyForm updateNodes={props.updateNodesAndEdges} emailId={emailId} bookName={fileName}  />
        </div>
        <ChapterForm nodeId={props.nodeId} chapterName={props.nodeName} /> 
        <div className="mt-auto">
          <button 
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
            onClick={handlePush}
          >
            Push Changes 
          </button>
        </div>
      </SidebarTemplate>
      </>
    )
  } else if (props.nodeType == "Topic") {
    return (
      <>
      <SidebarTemplate>
        <div className="mb-5">
          <SidebarHeader ElementType="node_text" ElementValue={props.nodeName} /> 
          <SidebarHeader ElementType="node_type" ElementValue={props.nodeType} /> 
        </div>

        <div className="mb-5">
          <HierarchyForm updateNodes={props.updateNodesAndEdges} emailId={emailId} bookName={fileName}  />
        </div>

        <TopicForm nodeId={props.nodeId} topicName={props.nodeName}/> 
        <div className="mt-auto">
          <button 
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
            onClick={handlePush}
          >
            Push Changes 
          </button>
        </div>
      </SidebarTemplate>
      </>
    )
  } else {

    return (
      <>
      <SidebarTemplate>
        <div className="mb-5"> 
          <SidebarHeader ElementValue={props.nodeName} /> 
          <SidebarHeader ElementValue={props.nodeType} /> 
        </div>

        <div className="mt-auto">
          <button 
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
            onClick={handlePush}
          >
            Push Changes 
          </button>
        </div> 
      </SidebarTemplate>

      </>
    )
  }
}

JsonSidebar.propTypes = {
  nodeName: PropTypes.string,  
  nodeType: PropTypes.string, 
  nodeId: PropTypes.string, 
  updateNodesAndEdges: PropTypes.func, 
}

export default JsonSidebar