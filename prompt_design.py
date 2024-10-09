import pandas as pd

# fetches the excel sheet located at : 
# https://docs.google.com/spreadsheets/d/1Kqrn5zw9MfDIYKqDUGnjAUYo2EVEjMlZ/edit?usp=sharing&ouid=101868315277228549653&rtpof=true&sd=true
# for the purposes of using the updated prompts
def prompts_csv(file_id: str) -> pd.DataFrame: 
    """
    file_id: str 
    Takes a google file_id assigned to the prompt_design excel file as a URI. 
    The function assumes that the provided file id is readable by anyone and 
    is an excel file. 
    Only works for our specific excel file. 
    """

    URL = "https://drive.google.com/uc?id=" + file_id 
    return pd.read_excel(
        URL, header=1, index_col=0
    )
