import streamlit as st
import requests
import json
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Constants
URL = os.getenv("API_URL", "http://localhost:8000")
USER_EMAIL = os.getenv("USER_EMAIL", "test.ai@yahoo.com")
PDF_NAME = os.getenv("PDF_NAME", "lbdl")
LANGUAGE_CODE = "en"

st.title("Streamlit JSON Editor App")

# Session state to persist selections and prevent refresh resets
if "chapter_title" not in st.session_state:
    st.session_state.chapter_title = None
if "node_id" not in st.session_state:
    st.session_state.node_id = None
if "node_json" not in st.session_state:
    st.session_state.node_json = None

# Fetch book chapters
st.header("Select a Chapter")
response = requests.get(f"{URL}/book_chapters/{USER_EMAIL}/{PDF_NAME}")
if response.status_code == 200:
    chapters = response.json()
    chapter_titles = chapters.get("titles", [])

    if not chapter_titles:
        st.error("No chapters found.")
    else:
        chapter_title = st.selectbox(
            "Choose a chapter:", chapter_titles, index=chapter_titles.index(st.session_state.chapter_title) if st.session_state.chapter_title in chapter_titles else 0
        )
        st.session_state.chapter_title = chapter_title

        # Fetch node count for the selected chapter
        response = requests.get(f"{URL}/get_node_count/{USER_EMAIL}/{PDF_NAME}/{chapter_title}")
        if response.status_code == 200:
            response_content = response.json()
            node_count = response_content.get("node_count", 0)

            if node_count > 0:
                st.header("Select a Node ID")
                node_id = st.number_input(
                    "Choose a node ID:",
                    min_value=0,
                    max_value=node_count - 1,
                    step=1,
                    value=st.session_state.node_id if st.session_state.node_id is not None else random.randint(0, node_count - 1)
                )
                st.session_state.node_id = node_id

                # Fetch the JSON content for the selected node
                if st.button("Fetch Node JSON"):
                    response = requests.post(
                        f"{URL}/get_text_node",
                        json={
                            "email_id": USER_EMAIL,
                            "filename": PDF_NAME,
                            "chapter_name": chapter_title,
                            "node_id": node_id,
                        },
                    )

                    if response.status_code == 200:
                        st.session_state.node_json = json.loads(response.json()["json_content"])
                    else:
                        st.error(f"Failed to fetch node JSON: {response.text}")
                        st.session_state.node_json = None

                if st.session_state.node_json:
                    node_json = st.session_state.node_json

                    # Display the "text" attribute as an uneditable textbox
                    st.subheader("Text Content")
                    st.markdown(node_json.get("text", ""))

                    # Create a DataFrame-like editor for specific keys
                    editable_keys = [
                        "concept", "sub_concept", "topic", "sub_topic", "heading_identifier",
                        "sub_heading_text", "heading_text", "text_type", "major_domains",
                        "root_concept", "sub_domains"
                    ]

                    editable_data = {key: node_json.get(key, "") for key in editable_keys}
                    user_modified_json = st.data_editor(
                        editable_data, use_container_width=True
                    )

                    # Allow the user to submit the modified JSON
                    if st.button("Submit Modified JSON"):
                        try:
                            # Update the original JSON with the modified values
                            for key in user_modified_json:
                                node_json[key] = user_modified_json[key]
                            with st.spinner("Processing JSON..."): 
                                submit_response = requests.post(
                                    f"{URL}/json_editor",
                                    json={
                                        "email_id": USER_EMAIL,
                                        "filename": PDF_NAME,
                                        "node_id": node_id,
                                        "chapter_name": chapter_title,
                                        "user_modified_json": json.dumps(node_json),
                                    },
                                )
                                if submit_response.status_code == 200:
                                    st.success("JSON updated successfully!")
                                    st.session_state.node_json = None  # Clear session state after successful update
                                else:
                                    st.error(f"Failed to update JSON: {submit_response.text}")
                        except Exception as e:
                            st.error(f"Error in processing JSON: {str(e)}")
            else:
                st.error("No nodes found for this chapter.")
        else:
            st.error(f"Failed to fetch node count: {response.text}")
        
        if st.button("Push Chapter Node Changes"):  
            response = requests.post(
                URL + "/rectify_update_chain", 
                json = {
                    "email_id": USER_EMAIL, 
                    "chapter_name": chapter_title, 
                    "filename": PDF_NAME, 
                } 
            ) 

            if response.status_code == 200: 
                st.success("Pushed JSON successfully to classifier")
            else: 
                st.error(f"Error occured: {json.dumps(response.json())}")
                

else:
    st.error(f"Failed to fetch chapters: {response.text}")

# import streamlit as st
# import json 
# import random
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv(override=True)

# URL : str = "http://localhost:8000"
# user_email: str = "test.ai@yahoo.com"
# pdf_name: str = "lbdl"


# language_code: str = "en"
# response = requests.get(URL + f"/book_chapters/{user_email}/{pdf_name}")
# if response.status_code == 200: 
#     chapters = response.json()

#     # user will select one chapter
#     chapter_title = chapters["titles"][4] 
#     response = requests.get(URL + f"/get_node_count/{user_email}/{pdf_name}/{chapter_title}") 
#     response_content: dict = response.json()

#     if response.status_code == 200: 
#         node_count: int = response_content.get("node_id")  

#         # user will also select a node id
#         node_id: int = random.randint(0, node_count)

#         # show user the json with the node id selected by him 
#         response = requests.post(
#             URL + "/get_text_node", 
#             json = {
#                 "email_id": user_email, 
#                 "filename": pdf_name, 
#                 "chapter_name": chapter_title, 
#                 "node_id": node_id, 
#             }
#         ) 

#         # Write the code for user to edit the json
#         user_modified_json: dict = "{}"

#         if response.status_code == 200: 
#             response = requests.post(
#                 URL + "/json_editor", 
#                 json = {
#                     "email_id": user_email, 
#                     "filename": pdf_name, 
#                     "node_id": node_id, 
#                     "chapter_name": chapter_title, 
#                     "user_modified_json": user_modified_json
#                 } 
#             ) 
#     else: 
#         print("could not fetch node count") 
#         print(json.dumps(response.json()))
    