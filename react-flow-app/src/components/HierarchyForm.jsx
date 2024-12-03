import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { TopicForm } from "./TopicForm";

const HierarchyForm = (props) => {
    const hierarchySegregation = ["topic-wise", "concept-wise", "heading-wise"]; 
    const hierarchyBox = "select-box-hierarchy"
    const [hierarchySelected, setHierarchySelected] = useState("topic-wise"); 
    const [updatedNodes, setUpdatedNodes] = useState(); 
    const [updatedEdges, setUpdatedEdges] = useState(); 
    const url = `http://localhost:8000/reactFlow/${hierarchySelected.split("-")[0]}/${props.emailId}/${props.bookName}`

    useEffect(() => {
        const fetchTreeContent = async(url) => {
            await fetch(url)
            .then(async (response) => await response.json())
            .then(async ([fetchedUpdatedNodes, fetchedUpdatedEdges]) => {
                setUpdatedNodes(fetchedUpdatedNodes); 
                setUpdatedEdges(fetchedUpdatedEdges); 
                props.updateNodes(updatedNodes, updatedEdges); 
            })
        }

        fetchTreeContent(url); 
    }, [hierarchySelected])

    return (
        <> 
            <label htmlFor={hierarchyBox} className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select the tree hierarchy</label>
            <select 
                id={hierarchyBox} 
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                defaultValue={hierarchySegregation[0]}
                onChange={(event) => setHierarchySelected(event.target.value)}
            >
                {hierarchySegregation.map((item, _) => {
                    return <option value={item} > {item} </option>
                })}
            </select>
        </> 
    ) 
}

HierarchyForm.propTypes = {
    emailId: PropTypes.string, 
    bookName: PropTypes.string, 
    updateNodes: PropTypes.func, 
} 

export default HierarchyForm; 