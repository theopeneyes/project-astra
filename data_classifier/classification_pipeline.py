import requests
from typing import Dict, List 

from prompts import (
    json_example, json_extractor_prompt, 
    definitions
) 

import re 
import json 

# loader to get json from the loaded dataframe 
def get_json(book_text: str, hf_token: str) -> Dict[str, List[str]]: 

    API_URL: str = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
        "x-wait-for-model": "true"
    }

    # chapter, definition, example 
    response = requests.post(
        API_URL, 
        headers=headers, 
        json = {
            "inputs": json_extractor_prompt.format(
               book_text, definitions, json_example,  
            ),  
            "parameters": {"max_new_tokens": 600, "temperature":0.1}
        }
    ).json() 

    extracted_json = response[0]["generated_text"].split("Extracted JSON:")[1].split("###")[0].strip()
    cleaned_response = re.sub(r'\s+', ' ', extracted_json)
    cleaned_response = cleaned_response.replace("'", '"')
    
    try:
        # Step 4: Parse and pretty print the cleaned JSON string
        data = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    return json.dumps(data)

    
# if __name__ == '__main__': 
#     book_text: str = '''
#     In computer science, an array is a data structure consisting of a collection of elements (values or variables), of same memory size, each identified by at least one array index or key. An array is stored such that the position of each element can be computed from its index tuple by a mathematical formula.[1][2][3] The simplest type of data structure is a linear array, also called a one-dimensional array.
#     For example, an array of ten 32-bit (4-byte) integer variables, with indices 0 through 9, may be stored as ten words at memory addresses 2000, 2004, 2008, ..., 2036, (in hexadecimal: 0x7D0, 0x7D4, 0x7D8, ..., 0x7F4) so that the element with index i has the address 2000 + (i × 4).[4] The memory address of the first element of an array is called first address, foundation address, or base address.
#     Because the mathematical concept of a matrix can be represented as a two-dimensional grid, two-dimensional arrays are also sometimes called "matrices". In some cases the term "vector" is used in computing to refer to an array, although tuples rather than vectors are the more mathematically correct equivalent. Tables are often implemented in the form of arrays, especially lookup tables; the word "table" is sometimes used as a synonym of array.
#     Arrays are among the oldest and most important data structures, and are used by almost every program. They are also used to implement many other data structures, such as lists and strings. They effectively exploit the addressing logic of computers. In most modern computers and many external storage devices, the memory is a one-dimensional array of words, whose indices are their addresses. Processors, especially vector processors, are often optimized for array operations.
#     Arrays are useful mostly because the element indices can be computed at run time. Among other things, this feature allows a single iterative statement to process arbitrarily many elements of an array. For that reason, the elements of an array data structure are required to have the same size and should use the same data representation. The set of valid index tuples and the addresses of the elements (and hence the element addressing formula) are usually,[3][5] but not always,[2] fixed while the array is in use.
#     The term "array" may also refer to an array data type, a kind of data type provided by most high-level programming languages that consists of a collection of values or variables that can be selected by one or more indices computed at run-time. Array types are often implemented by array structures; however, in some languages they may be implemented by hash tables, linked lists, search trees, or other data structures.
#     The term is also used, especially in the description of algorithms, to mean associative array or "abstract array", a theoretical computer science model (an abstract data type or ADT) intended to capture the essential properties of arrays.
#     '''.strip()

#     print(get_json(book_text=book_text, hf_token="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")) 

    

