import React from 'react'
import "../index.css"
import ChapterForm from './ChapterForm'
import {TopicForm} from './TopicForm'
import SidebarHeader from './SidebarHeader'
import SidebarTemplate from './SidebarTemplate'
import PropTypes from 'prop-types'
import BookForm from "./BookForm"


const JsonSidebar = (props) => {
  if (props.nodeType == "Book") {
    return (
      <>
      <SidebarTemplate> 
        <div className="mb-5">
          <SidebarHeader ElementType="node_text" ElementValue={props.nodeName} /> 
          <SidebarHeader ElementType="node_type" ElementValue={props.nodeType} /> 
        </div>
        <BookForm nodeId={props.nodeId} bookName={props.nodeName} />
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
        <ChapterForm nodeId={props.nodeId} chapterName={props.nodeName} /> 
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
        <TopicForm nodeId={props.nodeId} topicName={props.nodeName}/> 
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
      </SidebarTemplate>
      </>
    )
  }
}

JsonSidebar.propTypes = {
  nodeName: PropTypes.string,  
  nodeType: PropTypes.string, 
  nodeId: PropTypes.string, 
}

export default JsonSidebar