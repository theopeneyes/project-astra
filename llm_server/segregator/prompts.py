counting_prompt: str = """
Calculate the cumulative quantity of words across all provided texts related to a specified topic. 
The quantity of words is a numeric measure that sums the total number of words in all the given texts 
that pertain to the {}:  

{} 

###Output Format:###
Your output MUST be encapsulated within <count></count> tags 
"""