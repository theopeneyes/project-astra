import { useState } from "react"
import { questionTypes } from "./TopicForm"
import QuestionCount from "./QuestionCount" 


const BookForm = () => {
    return (
        <>
        <div className="mb-5">
        {questionTypes.map((value, index) => {
            return (
                <div className="mb-4">
                    <QuestionCount id={`${value}_${index}`} QuestionType = { value }/>
                </div> 
            ) 
        })}
        </div>
        </>
    )
}

export default BookForm 