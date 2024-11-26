import PropTypes from "prop-types"

const QuestionCount = (props) => {
    return (
        <> 
            <label 
                htmlFor="number-input" 
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >{ props.QuestionType }</label>
            <input type="number" id="number-input" aria-describedby="helper-text-explanation" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="0" min="0" required />
        </>
    )
}

QuestionCount.propTypes = {
    QuestionType: PropTypes.string, 
}

export default QuestionCount; 

