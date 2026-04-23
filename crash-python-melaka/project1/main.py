from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import unicodedata
import logging

app = FastAPI(title="Smart Text Sanitizer API")

# Add logging
# Transition to day 2 - Most of the time logging is done using decorator @
# logging configuration, from logging module
logging.basicConfig(
    filename="sanitizer.log",
    level=logging.ERROR,
    # time, level, log message
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# The input data is {"text":"Example text to be sanitized"}
class TextInput(BaseModel):
    text:str

# Tomorrow you will see decorator topic @
# Day 3, this will be replaced by decorator for validation
# Ensure that the received text is the right unicode encoder
def validate_utf8(text:str)->bool:
    try:
        text.encode("utf-8")
        return True
    except UnicodeEncodeError as e:
        logging.error(f"UTF-8 validation error: {e}")
        return False
    
@app.get("/")
def home():
    return {"message":"Smart Text Sanitizer API is running"}

# sanitize_text receive text of type string
# return data of type string
def sanitize_text(text:str)-> str:
    cleaned = text.strip() # Remove the whitespace at the beginning and end
    
    # Normalized the text
    # This will ensure the emoji and multiligual in tact
    normalized = unicodedata.normalize("NFC", cleaned) 

    return normalized

@app.post("/sanitize")
def sanitize(payload:TextInput):
    try:

        # Validation to check if it is a valid UTF-8 format
        is_valid = validate_utf8(payload.text)

        if not is_valid:
            raise ValueError("Input text is not valid UTF-8 encodable text")
        
        cleaned_text = sanitize_text(payload.text)

        return {
            # What what user send
            "original_text":payload.text,
            # After the sanitized operation
            "cleaned_text":cleaned_text,
            "normalized_form":"NFC",
            "is_valid_utf8":is_valid, # True or false
            "message":"Text sanitized successfully"
        }
    except Exception as e:
        logging.error(f"Sanitization error: {e}")
        raise HTTPException(status_code=400, detail=str(e))