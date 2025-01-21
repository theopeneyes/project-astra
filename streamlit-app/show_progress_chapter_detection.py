import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import base64
import re 
from io import BytesIO
from PIL import Image
from google.cloud import storage
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

chapter_pattern_detection_prompt: str = """
You are chapter pattern extraction bot. Your goal is to provide an abstract set of
rules that will describe a page which is at the beginning of a chapter.

### DEFINITIONS ###
left-aligned: the text is at the left side of the page.
right-aligned: the text is at the right side of the page.
center-algned: the text is at the middle of the page.
alignment: a property of text which can be left-aligned, right-aligned or center-aligned.

### INPUT ###
You will be provided with an image of a page which is the first page of a chapter.
Also referred to as a CHAPTER PAGE.

### TASK ###
Identify a set of ABSTRACT RULES to accurately describe the page.
These abstract rules MUST be book specific, which is to say that you can create rules
about the arrangement/alignment of text observed within the chapter page.

### INSTRUCTIONS ###
- All the rules MUST be in points without a heading.
- All the rules MUST start with "A Chapter page MUST" or "A Chapter page MAY"
depending on the necessity of the rule.
- Your rules MUST be enclosed between <rules> tag.
- Your rules MUST be abstract, not specific to the page.
- Your rule about the chapter title should specify the alignment of the text of the title.
"""

chapter_page_rule_aggregation_prompt: str = """
You are a chapter page rule aggregator prompt. Your goal is to create a set of abstract rules
that can identify a chapter page within a certain book.

### INPUT ###
Your input is going to be a list of rules, which have been observed in several chapter pages in the
book.

### TASK ###
You will be provided with a list of rules, all observed within different chapter pages of the book.
However, it's possible that there are small deviations within individual pages that create some
inonsistent rules across the chapter pages.

Your goal is to identify all unique rules and eliminate inconsistent rules and aggregate them
into a final set of rules to identify a chapter page.

### INSTRUCTIONS ###
- All the rules MUST be in points without a heading.
- All the rules MUST start with "A Chapter page MUST" or "A Chapter page MAY"
depending on the necessity of the rule.
- You MUST include all the MAY's from all three chapter titles collected since they are
possibilities.
- Your rules MUST be enclosed between <rules> tag.
- Your rules MUST be abstract, not specific to the page.
- Your rule about the chapter title should specify the alignment of the text of the title.

### RULE LIST ###
{}
"""

BUCKET_NAME: str = os.getenv("BUCKET_NAME") # name of the bucket 
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
gcs_client = storage.Client.from_service_account_json(".secrets/gcp_bucket.json")
bucket = gcs_client.bucket(BUCKET_NAME)

st.title("Chapter Page Prediction Viewer")

# Input for book name
BOOK_NAME = st.text_input("Enter the book name", "Machine-Learning-For-Absolute-Beginners")
EMAIL_ID = "test.fifth@yahoo.com"  # Replace with dynamic user email if needed

# File paths
font_index_path = os.path.join(EMAIL_ID, "fontwarehouse", BOOK_NAME, "chapter_image_fontwise_indices.json")
chapter_pages_path = os.path.join(EMAIL_ID, "book_sections", BOOK_NAME, "chapters.csv")
image_path = os.path.join(EMAIL_ID, "processed_image", BOOK_NAME + ".json")

gpt4omini = OpenAI(api_key=OPENAI_API_KEY)

messages: list[dict] = [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Generate your answer in English language.",
        },
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "",
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,{}",
          }
        }
      ]
    }
]

text_messages: list[dict] = [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "",
        },
      ]
    }
]

# Load data
try:
    # Load font indices
    font_index_blob = bucket.blob(font_index_path)
    with font_index_blob.open("r") as fp:
        font_indices = json.load(fp).get("chapter_indices", [])

    # Load chapter indices
    chapter_pages_blob = bucket.blob(chapter_pages_path)
    with chapter_pages_blob.open("r") as fp:
        df = pd.read_csv(fp)
    chapter_indices = df["index"].values.tolist()

    # Narrow down indices
    narrowed_down_pages = list(set(font_indices).intersection(set(chapter_indices)))

    # Display lists
    st.subheader("Page numbers identified by Font based algorithm")
    st.write(font_indices)

    st.subheader("Page numbers identified by Chapter based Indices")
    st.write(chapter_indices)

    st.subheader("Narrowed Down Page numbers")
    st.write(narrowed_down_pages)

    # Load images and model predictions
    image_blob = bucket.blob(image_path)
    with image_blob.open("r") as fp:
        images = json.load(fp)

    sample_features = []
    for page_no in narrowed_down_pages:
        book_item = images[page_no]
        img_data = base64.b64decode(book_item['img_b64'])
        img = Image.open(BytesIO(img_data)).convert('L')
        img_resized = img.resize((1240, 1240))
        img_array = np.array(img_resized).flatten()
        sample_features.append(img_array)

    sample_vector = np.array(sample_features)

    # Mock predictions for demo (replace with your model)
    predictions = np.random.choice([1], size=len(narrowed_down_pages))

    # Display predictions
    st.subheader("Model Predictions")
    prediction_data = {
        "Page Index": narrowed_down_pages,
        "Prediction": predictions.tolist()
    }
    st.write(pd.DataFrame(prediction_data))

    # Display pages side by side
    st.subheader("Predicted Chapter Pages")
    cols = st.columns(len(narrowed_down_pages))
    all_rules = []
    for col, (page_no, prediction) in zip(cols, zip(narrowed_down_pages, predictions)):
        if prediction == 1:
            book_item = images[page_no]
            img_data = base64.b64decode(book_item['img_b64'])
            img = Image.open(BytesIO(img_data)).convert('L')

            # Extract rules for the page
            messages[1]["content"][0]["text"] = chapter_pattern_detection_prompt
            messages[1]["content"][1]["image_url"]["url"] = (
                f"data:image/jpeg;base64,{book_item['img_b64']}")

            completions = gpt4omini.chat.completions.create(
                messages=messages,
                model="gpt-4o-mini",
                temperature=0.01
            )

            html_response = completions.choices[0].message.content
            document_rules = "No rules found"
            if re.findall(r"<rules>(.*?)</rules>", html_response, re.DOTALL):
                document_rules = re.findall(r"<rules>(.*?)</rules>", html_response, re.DOTALL)[0]
                all_rules.append(document_rules)

            with col:
                st.image(img, caption=f"Page {page_no}", use_container_width=True)
                st.markdown(f"**Rules:** {document_rules}")

    # Adding loading bar for rule extraction
    st.subheader("Aggregating Rules")
    progress_bar = st.progress(0)

    messages[0]["content"][0]["text"] = (
        chapter_page_rule_aggregation_prompt.format(str(all_rules)))
    completions = gpt4omini.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.01
    )

    html_response = completions.choices[0].message.content
    final_rules = "No aggregated rules found"
    if re.findall(r"<rules>(.*?)</rules>", html_response, re.DOTALL):
        final_rules = re.findall(r"<rules>(.*?)</rules>", html_response, re.DOTALL)[0]

    st.success("Rules extraction and aggregation complete!")
    st.markdown(f"### Final Aggregated Rules:\n{final_rules}")

    chapter_page_indices = [54, 34, 12]

    st.subheader("Pages classified as Chapter pages.")
    cols = st.columns(len(narrowed_down_pages))
    for col, page_no in zip(cols, chapter_page_indices): 
        book_item = images[page_no]
        img_data = base64.b64decode(book_item['img_b64'])
        img = Image.open(BytesIO(img_data)).convert('L')

        with col: 
            st.image(img, caption=f"Page {page_no}", use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {e}")