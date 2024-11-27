import PropTypes from "prop-types";
import {useEffect, useState} from "react"; 

const Glider = (props) => {
    const [chapterWeight, setChapterWeight] = useState(10); 
    const [maxWeight, setMaxWeight] = useState(100); 

    useEffect(() => {
        let proportionOccupied = 0; 
        for(let i = 0; i < localStorage.length; i++) {
            if (localStorage.key(i).startsWith("chapter")) {
                let chapterNode = JSON.parse(localStorage.getItem(localStorage.key(i))) 
                proportionOccupied += chapterNode.nodeContent.gliderValue
            }
        }
        setMaxWeight(100 - proportionOccupied); 
    })

    const onChangeCallback = (e) => {
        setChapterWeight(e.target.value); 
        props.onChangeFunction(e); 
    }

    if(maxWeight > 0) {
        return (
            <>
            <div className="relative mb-6">
                <label htmlFor="large-range" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Chapter Weights</label>
                <input 
                    id="large-range" 
                    type="range" 
                    value={chapterWeight} 
                    className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer range-lg dark:bg-gray-700" 
                    onChange={onChangeCallback}
                    min = "0" 
                    max = {maxWeight} 
                />

                <span className="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">Min 0 %</span>
                <span className="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">Max {maxWeight} %</span>
            </div>
            </>
        )
    } else {

        return (
            <>
            <div className="relative mb-6">
                <label htmlFor="large-range" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Chapter Weights</label>
                <input 
                    id="large-range" 
                    type="range" 
                    value={chapterWeight} 
                    className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer range-lg dark:bg-gray-700" 
                    onChange={onChangeCallback}
                    min = "0" 
                    max = "0" 
                    disabled
                />

                <span className="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">Min 0 %</span>
                <span className="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">Max 0 %</span>
            </div>
            </>
        )

    }
}

Glider.propTypes = {
    onChangeFunction : PropTypes.func, 
}

export default Glider; 

