const SidebarTemplate = ({children}) => {
    return (
        <>
            <aside id="default-sidebar" className="fixed top-0 right-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
            <div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
                <ul className="space-y-2 font-medium"></ul>
                <form className="max-w-sm mx-auto">
                    <div className="mb-5">
                        {children}
                    </div>
                </form>
            </div> 
            </aside>
        </>
    )
}

export default SidebarTemplate