import { questionTypes } from "./QuestionTypes"; 
import { useState } from "react"; 
import QuestionCount from "./QuestionCount" 
import PropTypes from "prop-types";

const questionToKeyMap = {
    "True/False": "trueFalse", 
    "Fill in the blanks": "fillInTheBlanks", 
    "Short Question Answer": "shortQuestionAnswer", 
    "Multiple Choice": "multipleChoice", 
    "Computational Questions": "computationQuestion", 
    "Software Code Questions": "softwareCodeQuestion", 
}

const BookForm = (props) => {
    const [storageContent, setStorageContent] = useState({
        nodeName: props.bookName, 
        nodeType: "book", 
        nodeId: props.nodeId, 
        nodeContent: {
            fillInTheBlanks: 0, 
            trueFalse: 0, 
            shortQuestionAnswer: 0, 
            multipleChoice: 0, 
            computationQuestion: 0, 
            softwareCodeQuestion: 0, 
        }, 
    })

    const onQuestionCountChange = (e) => {
        const questionType = questionToKeyMap[e.target.id]; 
        const questionCount = e.target.value; 

        setStorageContent((prev) => {
            return {...prev, 
                nodeName: props.bookName, 
                nodeId: props.nodeId, 
                nodeContent: {
                ...prev.nodeContent, [questionType]: parseInt(questionCount)
            }}
        })
    }

    const onSubmitBookData = (e) => {
        e.preventDefault(); 
        localStorage.setItem(`book-${props.bookName}`, JSON.stringify(storageContent)); 
    }

    return (
        <>
        <form onSubmit= {onSubmitBookData} className="max-w-sm mx-auto">
            <div className="mb-5">
            {questionTypes.map((value, index) => {
                return (
                    <div className="mb-4">
                        <QuestionCount 
                            key={value}
                            onChangeFunction={onQuestionCountChange} 
                            id={`${value}_${index}`} 
                            QuestionType = { value }
                        />
                    </div> 
                ) 
            })}
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

BookForm.propTypes = {
    bookName: PropTypes.string, 
    nodeId: PropTypes.string, 
}

export default BookForm 