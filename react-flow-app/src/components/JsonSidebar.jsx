import React from 'react'
import "../index.css"
import ChapterForm from './ChapterForm'
import TopicForm from './TopicForm'

const JsonSidebar = (props) => {
  if(props.nodeType == "Chapter") {
    return (
      <>
      <form className="max-w-sm mx-auto">
          <div className="mb-5">
            <h3>Node Name: { props.nodeName } </h3>
            <h3>Node Type: { props.nodeType } </h3> 
            <ChapterForm/> 
          </div>
      </form>
      </>
    )
  } else if (props.nodeType == "Topic") {
    return (
      <>
      <form className="max-w-sm mx-auto">
          <div className="mb-5">
            <h3>Node Name: { props.nodeName } </h3>
            <h3>Node Type: { props.nodeType } </h3> 
            <TopicForm/> 
          </div>
      </form>
      </>
    )
  } else {

    return (
      <>
      <form className="max-w-sm mx-auto">
          <div className="mb-5">
            <h3>Node Name: { props.nodeName } </h3>
            <h3>Node Type: { props.nodeType } </h3> 
          </div>
      </form>
      </>
    )

  }
  
}

export default JsonSidebar