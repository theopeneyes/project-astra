import SelectBox from "./SelectBox"
import { questionTypes } from "./QuestionTypes";
import { useState } from "react"; 
import PropTypes from "prop-types";


const preferenceLevel = ["Ignore", "High", "Medium", "Low" ]; 

const TopicForm = (props) => {
    const [storageContent, setStorageContent] = useState({
        nodeName: props.topicName, 
        nodeType: "topic", 
        bookName: props.nodeId.split("=")[2].split(":")[0], 
        chapterName: props.nodeId.split("=")[2].split(":")[1],  
        nodeId: props.nodeId, 
        nodeContent: {
            preferenceLevel: "Ignore", 
            questionType: "True/False", 
        },  
    })

    const onTopicSubmit = (e) => {
        e.preventDefault(); 
        localStorage.setItem(`topic-${props.topicName}`, JSON.stringify(storageContent))
    }

    const onTopicMetadataChange = (e) => {
        const metadataType = e.target.id; 
        const optionSelected = e.target.value; 

        setStorageContent((prev) => {
            return {...prev, 
                nodeName: props.topicName, 
                bookName: props.nodeId.split("=")[2].split(":")[0], 
                chapterName: props.nodeId.split("=")[2].split(":")[1],  
                nodeId: props.nodeId, 
                nodeContent: {
                ...prev.nodeContent, 
                [metadataType]: optionSelected, 
            }}; 
        })
    }

    return (
        <>
        <form onSubmit={onTopicSubmit} className="max-w-sm mx-auto"> 
            <div className="mb-5">
                <SelectBox 
                    category="preferenceLevel"
                    labelText ="Select your preference of the given topic" 
                    Vector={preferenceLevel} 
                    onChangeFunction={onTopicMetadataChange}
                /> 
            </div>
            <div className="mb-5">
                <SelectBox 
                    category="questionType"
                    labelText="Select any one of the question types you require for the given topic" 
                    Vector={questionTypes} 
                    onChangeFunction={onTopicMetadataChange}
                /> 
            </div>
            <div className="mb-5"> 
                <button 
                    type="submit" 
                    className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                >Update
                </button>
            </div> 
        </form> 
        </>
    )
}

TopicForm.propTypes = {
    topicName: PropTypes.string, 
    nodeId: PropTypes.string, 
}

export { TopicForm, questionTypes } 