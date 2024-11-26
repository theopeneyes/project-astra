import { useState, useEffect} from "react"; 

const useFetchNodes = (url) => {
  const [fetchedNodes, setFetchedNodes] = useState([]); 
  const [fetchedEdges, setFetchedEdges]  = useState([]);  

  useEffect(() => {
    const fetchUrlData = async () => {
      await fetch(url).then(
        async (response) => await response.json()
      ).then(async ([ initialNodes, initialEdges ]) => {
        setFetchedNodes(initialNodes)
        setFetchedEdges(initialEdges)
      })
    }

    fetchUrlData()
  }, [url])

  return {initialNodes: fetchedNodes, initialEdges: fetchedEdges }
}

export { useFetchNodes }; 