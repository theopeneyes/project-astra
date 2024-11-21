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
        <div className="mb-5">
            <SelectBox labelText ="Select your preference of the given topic" Vector={preferenceLevel} /> 
        </div>
        <div className="mb-5">
            <SelectBox labelText="Select any one of the question types you require for the given topic" Vector={questionTypes} /> 
        </div>

        </>
    )
}

export { TopicForm, questionTypes } 