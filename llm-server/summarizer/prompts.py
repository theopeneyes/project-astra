summarization_prompt: str = """
### SYSTEM ### 
You MUST ensure that the summarization is in {} language. 

You are a summarization bot. Your goal is to take the chapter content within a book and 
generate a detailed summary from the given text. Here is the text content provided below:  

### Text to summarize ### 
{}

### Instruction ### 
You must enclose the summary within <summary> tags in your output. 

### Summary ###
"""