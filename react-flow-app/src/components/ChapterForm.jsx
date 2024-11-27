import {useState} from "react"; 
import Glider from './Glider';  
import PropTypes from "prop-types";

const ChapterForm = (props) => {

    const [storageNode, setStorageNode] = useState({
        nodeName: props.chapterName, 
        nodeType: "chapter", 
        nodeId: props.nodeId, 
        nodeContent: {
            gliderValue: 0, 
        },  
    }) 


    const onGliderSubmit = (e) => {
        e.preventDefault(); 
        localStorage.setItem(`chapter-${props.chapterName}`, JSON.stringify(storageNode)); 
    }

    const onGliderChangeFunction = (e) => {
        
        setStorageNode((prev) => ({
            ...prev, 
            nodeName: props.chapterName, 
            nodeId: props.nodeId, 
            nodeContent: { 
                ...prev.nodeContent, 
                gliderValue: parseInt(e.target.value)  
            },
        }));
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
    nodeId: PropTypes.string, 
}

export default ChapterForm 