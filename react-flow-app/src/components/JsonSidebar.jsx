import React from 'react'
import "../index.css"
import ChapterForm from './ChapterForm'
import TopicForm from './TopicForm'
import SidebarHeader from './SidebarHeader'
import SidebarTemplate from './SidebarTemplate'
import PropTypes from 'prop-types'


const JsonSidebar = (props) => {
  if(props.nodeType == "Chapter") {
    return (
      <>
      <SidebarTemplate> 
        <SidebarHeader ElementValue={props.nodeName} /> 
        <SidebarHeader ElementValue={props.nodeType} /> 
        <ChapterForm/> 
      </SidebarTemplate>
      </>
    )
  } else if (props.nodeType == "Topic") {
    return (
      <>
      <SidebarTemplate>
        <SidebarHeader ElementValue= {props.nodeName } /> 
        <SidebarHeader ElementValue={props.nodeType} /> 
        <TopicForm/> 
      </SidebarTemplate>
      </>
    )
  } else {

    return (
      <>
      <SidebarTemplate>
        <SidebarHeader ElementValue={props.nodeName} /> 
        <SidebarHeader ElementValue={props.nodeType} /> 
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