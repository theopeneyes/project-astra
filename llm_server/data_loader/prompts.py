# prompts required to convert the images of books into html documents 
validation_prompt: str = """
Task Instructions
Reflect on Previous Attempts:
Think about any past responses to similar tasks. Identify what went well and any common mistakes. Plan adjustments to avoid repeating errors.
Thought Process (Step-by-Step Reasoning):
Break down the task step-by-step to ensure clarity and accuracy.
{}
Actions:
Step 1: Convert  the given page into HTML using the following prompt 
{}
Step 2: Validate the outcomes from the lens of syntax, structure, and W3C markup validation and consolidate them as described in 
{}
Observation:
After each step, check if the output aligns with task requirements. Adjust if necessary.
Reflection:
Review the completed answer. Reflect on whether all aspects of the prompt were addressed accurately and concisely.
Revise if any critical detail is missing or any part of the response fails to meet the prompt’s requirements.
"""

# clause prompts
previous_clause_prompt: str = " and if one doesn't exist then use '{}' as the title"

clause_prompt: str = "If one doesn't exist then use '{}' as the title. "
# main prompts
generation_prompt: str = """
You are a HTML converter bot. Your TASK is to convert text and image as text from a given image
of a page from a book into a HTML document.

Here are further detailed instructions:
Input: You will be given an image from a page of a book. This page will be part of a Chapter from a
book containing sections, and sub-sections and within subsections will be units of Paragraphs and Images. Images could be of Types: [Chart, Diagram, Tables]

Your goal is to extract text from the image of a page from a book conserving the hierarchical
nature of the way the page is structured. You will use HTML tags to conserve the hierarchy.

Follow the following steps when encountered with a page:

Step 1: Determine if the page contains a chapter heading. {} Write the title between <title>
tags. NOTE that each page must only have ONE unique title and VERIFY that the chosen title is a
chapter title and not a section heading or a sub section heading.

Step 2: Determine if the page contains any section headings. {} Write the section headings between <h1> tags. The page can have multiple section headings. VERIFY that the chosen <h1> heading
is a section heading and not a chapter heading or a sub section heading.

Step 3: Identify if the page has any sub section headings. {} Write the sub section headings between <h2> tags.
The page can have multiple sub section headings. VERIFY that the chosen <h2> heading is a sub
section heading and not a chapter heading or a section heading.

In any of these above steps, if you encounter a paragraph text, then write the paragraphs identified between <p> tags.

Step 4: Identify if there are any images and classify the type of image into one of 3 categories:
diagram, chart or table.

The definitions of which are given below:

## Definitions
chart: A chart (sometimes known as a graph) is a graphical representation for data visualization,
in which the data is represented by symbols, such as bars in a bar chart, lines in a line chart,
or slices in a pie chart
table: A table is an arrangement of information or data, typically in rows and columns,
or possibly in a more complex structure.
diagram: Any image that isn't a table or a chart is a diagram.

Step 5: Once you have identified the type of image, convert the image into text by explaining the
relevance of the image given the context of the surrounding text and tag them within their
respective tags. For example: encapsulate chart with <chart> tags, diagrams with <diagram>
If the image contains a table, extract the contents of the table as is, and write between  
<table> tags.

You MUST only use the following list of tags:
[<p>, <h1>, <h2>, <table>, <td>,  <tr>, <th>, <diagram>, <chart>, <title>]

## Instructions
Your outcomes MUST be simple and unambigous.

## Incentives
You will recieve a tip of $$$ for correct conversion
You will be penalized if you fail to conver the document effectively
"""
