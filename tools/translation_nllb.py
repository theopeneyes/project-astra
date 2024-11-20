from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv
load_dotenv()
import os

token = os.getenv("HF_TOEN")
language_codes={
    "English": "eng_Latn",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva"
}

# if source_language is not equal to desired language then 

def nllb_translate(source_text: str, source_language: str, desired_language: str):
    source_lang_code = language_codes.get(source_language)
    desired_lang_code = language_codes.get(desired_language)
    if source_lang_code != desired_lang_code:
        tokenizer = AutoTokenizer.from_pretrained(
    "facebook/nllb-200-distilled-600M", token=token, src_lang='eng_Latn')
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", token=token)
        inputs = tokenizer(source_text, return_tensors='pt')
        
        translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(desired_language), max_length=30)

        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    else: 
        return source_text 