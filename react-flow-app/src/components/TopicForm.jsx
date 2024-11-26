import SelectBox from "./SelectBox"
import { questionTypes } from "./QuestionTypes";
import PropTypes from "prop-types";


const preferenceLevel = ["Ignore", "High", "Medium", "Low" ]; 

const TopicForm = (props) => {
    const onTopicSubmit = (e) => {
        e.preventDefault(); 
    }

    const [storageContent, setStorageContent] = useState({
        nodeName: props.topicName, 
        nodeType: "topic", 
        nodeContent: null,  
    })

    const [nodeContent, setNodeContent] = useState({
        preferenceLevel: null, 
        questionType: null, 
    })

    const onTopicMetadataChange = (e) => {
        const metadataType = e.target.id; 
        const optionSelected = e.target.value; 
        
        setNodeContent((prev) => {
            return {...prev, [metadataType]: optionSelected}
        })

        setStorageContent((prev) => {
            return {...prev, nodeContent: nodeContent}; 
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
}

export { TopicForm, questionTypes } 