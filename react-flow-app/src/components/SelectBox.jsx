import PropTypes from "prop-types"

const SelectBox = (props) => {
    return (
        <>
        <form className="max-w-sm mx-auto">
            <label for="question-type" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{ props.labelText }</label>
            <select 
                id="question-type" 
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                defaultValue={props.Vector[0]}
            >
                {props.Vector.map((item, _) => {
                    return <option value={item} > {item} </option>
                })}
            </select>
        </form>
        </>
    )
}

SelectBox.propTypes = {
    labelText: PropTypes.string, 
    Vector: PropTypes.array
}

export default SelectBox 