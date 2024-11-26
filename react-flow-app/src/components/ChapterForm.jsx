import {useState} from "react"; 
import Glider from './Glider';  
import PropTypes from "prop-types";

const ChapterForm = (props) => {

    const [storageNode, setStorageNode] = useState({
        nodeName: props.chapterName, 
        nodeType: "chapter", 
        nodeContent: null,  
    }) 

    const [nodeContent, setNodeContent] = useState({
        gliderValue: null, 
    })

    const onGliderSubmit = (e) => {
        e.preventDefault(); 
    }

    const onGliderChangeFunction = (e) => {
        setNodeContent((prev) => {
            return {...prev, gliderValue: parseInt(e.target.value)}
        })

        setStorageNode((prev) => {
            return {...prev, nodeContent: nodeContent}
        })
    }

    return (
        <>
        <div >
            <form onSubmit = {onGliderSubmit} className="max-w-sm mx-auto">
                <div className="mb-5">
                    <Glider onChangeFunction = {onGliderChangeFunction} /> 
                </div>
                <div className="mb-5"> 
                    <button 
                        type="submit" 
                        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                    >Update
                    </button>
                </div> 
            </form>
        </div> 
        </>
    )
}

ChapterForm.propTypes = {
    chapterName: PropTypes.string, 
}

export default ChapterForm 