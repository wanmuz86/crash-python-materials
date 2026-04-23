# Import the unicodedata module to be able to read the files 
# specified as encoding
import unicodedata

filename = "mixed_text.txt"

try:
    # Open the file , on read mode ("r") using utf-8 encoding
    # "r" -> Read only -> return string
    # "rb" -> Read as b inary (image/pdf) -> return binary
    # "r+" -> Read and write mode

    # errors ="replace"-> will replace the unread cjaracters with square instead of crashing
    with open(filename,"r", encoding="utf-8", errors="replace") as file:
        content = file.read()
    print("=== Original content")
    print(content)
# Error handling if unable to read the file
# Wrong formating
except UnicodeDecodeError as e:
    print("Encoding error while reading file:")
    print(e)
    content= ""

#Error handling if unable to open the file
# File not found
except FileNotFoundError:
    # f in the beginning indicate interpolation
    # the value of filename will be replaced
    print(f"File not found: {filename}")
    content = ""


if content:
    # to normalized the content so the value for é is intepreted the same as u301
    # NFC =  Normalization Form Canonical Decomposition (Way to normalized it)
    normalized_content = unicodedata.normalize("NFC", content)
    print("\n====Normalized Content (NFC)===")
    print(normalized_content)

word1 = "Kafé" 
word2 = "Kafe\u0301" # e + combining accent (e ekor)

#Without normalization
print("\n=== Comparison before normalization ===")
print(word1)
print(word2)
print("Are they equal? ", word1 == word2)

normalized_word1 = unicodedata.normalize("NFC",word1)
normalized_word2 = unicodedata.normalize("NFC",word2)

#With normalization
print("\n=== Comparison after normalization ===")
print("normalized_word1: ",normalized_word1)
print("normalized_word2: ",normalized_word2)
print("Are they equal? ", normalized_word1 == normalized_word2)