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
          <SidebarHeader ElementValue={props.nodeName} /> 
          <SidebarHeader ElementValue={props.nodeType} /> 
        </div>
        <BookForm />
      </SidebarTemplate>
      </>
    )

  }
  else if(props.nodeType == "Chapter") {
    return (
      <>
      <SidebarTemplate> 
        <div className="mb-5">
          <SidebarHeader ElementValue={props.nodeName} /> 
          <SidebarHeader ElementValue={props.nodeType} /> 
        </div>
        <ChapterForm/> 
      </SidebarTemplate>
      </>
    )
  } else if (props.nodeType == "Topic") {
    return (
      <>
      <SidebarTemplate>
        <div className="mb-5">
          <SidebarHeader ElementValue={props.nodeName} /> 
          <SidebarHeader ElementValue={props.nodeType} /> 
        </div>
        <TopicForm/> 
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
  nodeType: PropTypes.string
}

export default JsonSidebar