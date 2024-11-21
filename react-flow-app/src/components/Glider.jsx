import {useState} from "react"; 

const Glider = () => {
    const [chapterWeight, setChapterWeight] = useState(10); 

    const onChangeCallback = (e) => {
        setChapterWeight(e.target.value); 
    }

    return (
        <>
        <div className="relative mb-6">
            <label for="large-range" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Chapter Weights</label>
            <input 
                id="large-range" 
                type="range" 
                value={chapterWeight} 
                className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer range-lg dark:bg-gray-700" 
                onChange={onChangeCallback}
            />

            <span className="text-sm text-gray-500 dark:text-gray-400 absolute start-0 -bottom-6">Min 0 %</span>
            <span className="text-sm text-gray-500 dark:text-gray-400 absolute end-0 -bottom-6">Max 100 %</span>
        </div>
        </>
    )
}

export default Glider; 