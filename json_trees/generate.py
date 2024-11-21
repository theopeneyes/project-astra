from collections import defaultdict

class JSONParser:
    def __init__(self, book_name): 
        self.book_name = book_name 
        
    def _get_child_node(self, parent_map, search_key, default_value):
        """
        Get a child node from a parent map. If the search key does not exist, it initializes it with the default value.

        Args:
            parent_map (dict): The parent map to search within.
            search_key (str): The key to search for.
            default_value (dict or set): The default value to initialize if the key does not exist.

        Returns:
            dict or set: The child node corresponding to the search key.
        """
        if not search_key:
            search_key = "default"
        
        if search_key not in parent_map:
            parent_map[search_key] = default_value
        
        return parent_map[search_key]

    def to_tree(self, vector_book_json):
        """
        Converts a list of vector book JSON objects into a hierarchical tree structure.

        Args:
            vector_book_json (list): List of JSON objects with keys 'heading_identifier',
                                    'heading_text', and 'sub_heading_text'.

        Returns:
            dict: A nested dictionary representing the tree structure.
        """
        book_tree = defaultdict(dict)
        for book_json in vector_book_json:
            heading_sub_tree = self._get_child_node(book_tree, book_json['heading_identifier'], defaultdict(set))
            sub_heading_tree = self._get_child_node(heading_sub_tree, book_json['heading_text'], defaultdict(set))
            text_list = self._get_child_node(sub_heading_tree, book_json['sub_heading_text'], set())
            text_list.add(book_json['text'])
        
        return book_tree 
    
    def _connect_parent_child(self, parent_title, child_titles, origin, category):
        nodes = []
        edges = []
        origins = []
        
        child_node_y_distance = 2000 / len(child_titles) 
        child_node_y_position = origin.get("y") - child_node_y_distance 
        for child_title in child_titles: 
            # add the child node
            node_origin = {"y": int(child_node_y_position), "x": origin.get("x") + 200}
            origins.append(node_origin)

            nodes.append({
                "id": f"{category}:{child_title}", 
                "position": node_origin, 
                "sourcePosition": "right", 
                "targetPosition": "left", 
                "data": {
                    "label": child_title,  
                }
            })

            child_node_y_position += child_node_y_distance

            # connect the two nodes. 
            edges.append({
                "id": f"{parent_title}={category}:{child_title}", 
                "source": parent_title, 
                "target": f"{category}:{child_title}", 
            })
        
        return nodes, edges, origins
    
    def parse_tree(self, main_tree): 
        origin = {
            "x": 0, "y": 0
        }

        nodes = [{
            "id": self.book_name, 
            "sourcePosition": "right", 
            "targetPosition": "left", 
            "position": origin, 
            "data": {
                "label": self.book_name, 
            }
        }] 
        edges = []

        # creating nodes and edges that connect book name with chapter titles
        chapter_nodes, chapter_edges, chapter_origins = self._connect_parent_child(
            self.book_name, main_tree.keys(), origin=origin, category="chapter",          
        )

        nodes.extend(chapter_nodes) 
        edges.extend(chapter_edges)
        
        # do this for every chapter sub tree 
        for idx, chapter_title in enumerate(main_tree.keys()): 
            chapter_child_tree = main_tree[chapter_title]
            heading_nodes, heading_edges, heading_origins = self._connect_parent_child(
                f"chapter:{chapter_title}", 
                chapter_child_tree.keys(), 
                origin = chapter_origins[idx], 
                category="topic", 
            )

            nodes.extend(heading_nodes) 
            edges.extend(heading_edges)
            
            for jdx, heading_title in enumerate(chapter_child_tree.keys()): 
                heading_child_tree = chapter_child_tree[heading_title] 
                
                sub_heading_nodes, sub_heading_edges, sub_heading_origins = self._connect_parent_child(
                   f"topic:{heading_title}", 
                   heading_child_tree.keys(), 
                   origin = heading_origins[jdx], 
                   category="sub_heading"
                )

                nodes.extend(sub_heading_nodes)
                edges.extend(sub_heading_edges)
            
                for kdx, sub_heading_title in enumerate(heading_child_tree.keys()):
                    text_node_names =  heading_child_tree[sub_heading_title]
                    text_nodes, text_edges, _ = self._connect_parent_child(
                        f"sub_heading:{sub_heading_title}", 
                        text_node_names, 
                        origin = sub_heading_origins[kdx], 
                        category="text" 
                    )

                    nodes.extend(text_nodes)
                    edges.extend(text_edges)
    
        return nodes, edges 


                    
                   

                    
            

        

            

            
            


