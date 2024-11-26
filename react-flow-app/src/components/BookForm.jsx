import { questionTypes } from "./TopicForm"
import QuestionCount from "./QuestionCount" 


const BookForm = () => {
    return (
        <>
        <form className="max-w-sm mx-auto">
            <div className="mb-5">
            {questionTypes.map((value, index) => {
                return (
                    <div className="mb-4">
                        <QuestionCount id={`${value}_${index}`} QuestionType = { value }/>
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

export default BookForm 