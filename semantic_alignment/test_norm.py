def semantic_expansion(original_list, deduplicated_list):
    """
    Expand a deduplicated list back to the original list's length 
    by repeating semantically similar items.
    
    Args:
    original_list (list): The original input list with duplicates and variations
    deduplicated_list (list): The list of unique semantic categories
    
    Returns:
    list: Expanded list with repeated semantic categories
    """
    # Create a mapping of original items to their semantic categories
    def find_semantic_match(item, semantic_categories):
        # Convert to lowercase for case-insensitive matching
        item_lower = item.lower()
        
        for category in semantic_categories:
            # Check if the category is a substring or semantically close
            if (category.lower() in item_lower or 
                any(word.lower() in item_lower for word in category.lower().split())):
                return category
        
        return item  # Return original if no match found
    
    # Generate the expanded list
    expanded_list = []
    
    for original_item in original_list:
        # Find the semantic match from the deduplicated list
        semantic_match = find_semantic_match(original_item, deduplicated_list)
        expanded_list.append(semantic_match)
    
    return expanded_list

# Example usage
original_input = ['Machine Learning', 'ML', 'machine Learning (ml)', 'natural language processing', 'nlp', 'random shit 1', 'random shit 2', 'random shit 3']
deduplicated_input = ['Machine learning', 'natural language processing', 'random shit']

result = semantic_expansion(original_input, deduplicated_input)
print(result)
