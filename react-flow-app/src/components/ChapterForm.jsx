const ChapterForm = () => {
    return (
        <>
        <div >
            <form className="max-w-sm mx-auto">
                <div className="mb-5">
                    <label for="large-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                        Chapter Weights
                    </label>
                    <input type="text" id="large-input" className="block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
                </div>
            </form>
        </div> 
        </>
    )
}

export default ChapterForm 