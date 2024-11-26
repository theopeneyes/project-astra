import SelectBox from "./SelectBox"


const questionTypes = [ 
    "True/False",
    "Fill in the blanks",
    "Short Question Answer",
    "Multiple Choice",
    "Computational Questions",
    "Software Code Questions",
]; 

const preferenceLevel = ["Ignore", "High", "Medium", "Low" ]; 

const TopicForm = () => {
    return (
        <>
        <form className="max-w-sm mx-auto"> 
            <div className="mb-5">
                <SelectBox labelText ="Select your preference of the given topic" Vector={preferenceLevel} /> 
            </div>
            <div className="mb-5">
                <SelectBox labelText="Select any one of the question types you require for the given topic" Vector={questionTypes} /> 
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

export { TopicForm, questionTypes } 