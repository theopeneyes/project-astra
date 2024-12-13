semantic_normalization_prompt = """

You are a normalizer bot. Your duties include reading through the below list and to filter out the words from this list that can have similar semantic meaning and remove them. 
list = {}

For example, "passing the time", "time-pass" and "timepass" all mean the same thing. In such cases, keep the word that represents the entity most clearly. 

Similarly, "Deep learning" and "DL" mean the same thing. In this case, it is an abbreviation of the other, but they are essentiallly the same thing. In this case, remove the abbreviation and keep the original entity. 

In any other cases, if there are two semantically similar words in the list, keep the one which represents the entity more accurately.

FOR EXAMPLE, 
A list like ['Deep Learning', 'Deep Learning (DL)', 'DL', 'Neural Networks', 'Neural Network', 'NN', 'Activation functions', 'reinforcement learning] should be filtered like this:
['Deep Learning', 'Neural Network', 'Activation functions', 'reinforcement learning']

Your output should contain only a list.
""" 

snp = """

You are tasked with semantic normalization of the following list. Your goal is to ensure each concept is represented by the most precise and appropriate term, removing redundancy caused by semantic overlap. 

Normalization Rules:
1. **Deduplication of Similar Terms:** Identify semantically similar words or phrases and keep only the one that most clearly and accurately represents the concept.
   - Example: ["passing the time", "time-pass", "timepass"] → Keep "passing the time."
2. **Abbreviations and Full Forms:** Retain the full form of a term if one entry is an abbreviation or shorthand of another.
   - Example: ["Deep Learning", "DL"] → Keep "Deep Learning."
3. **Precision in Representation:** For other cases of similarity, retain the term that is more accurate, descriptive, or widely understood.
   - Example: ["Neural Networks", "Neural Network", "NN"] → Keep "Neural Network."

Example Input:
['Deep Learning', 'Deep Learning (DL)', 'DL', 'Neural Networks', 'Neural Network', 'NN', 'Activation functions', 'reinforcement learning']

Example Output:
['Deep Learning', 'Neural Network', 'Activation functions', 'reinforcement learning']

Normalize the following list according to the rules and return ONLY the filtered list as your output:
list = {}


"""
snp2 = """
You are a semantic normalization bot designed to process a list of terms, identify semantically similar entries, and refine the list to ensure clarity and consistency. 

Guidelines:
1. **Semantic Similarity:** Identify terms with similar meanings and retain only one representative term.
   - Example: ["passing the time", "time-pass", "timepass"] → Keep "passing the time."
2. **Abbreviations:** If one term is an abbreviation or shorthand for another, retain the full form and remove the abbreviation.
   - Example: ["Deep Learning", "DL"] → Keep "Deep Learning."
3. **Precision and Accuracy:** When terms have overlapping or identical meanings, prioritize the term that is most precise and widely recognized.
   - Example: ["Neural Networks", "Neural Network", "NN"] → Keep "Neural Network."

Example:
Input: ['Deep Learning', 'Deep Learning (DL)', 'DL', 'Neural Networks', 'Neural Network', 'NN', 'Activation functions', 'reinforcement learning']
Output: ['Deep Learning', 'Neural Network', 'Activation functions', 'reinforcement learning']

Your task is to process the list below and return a filtered version containing only the most accurate and representative terms. Return ONLY the single list.
list = {}

"""
