#Using requests module / library
import requests
import json

url = "https://jsonplaceholder.typicode.com/users"
output_file = "users_output.json"
try:

    # get -> method GET of the API
    # pay attention later for API methods, GET , POST, PUT , DELETE
    # cross check with slide for example requests.post (file upload)
    # timeout 10 => max 10s
    response = requests.get(url, timeout=10)
    response.raise_for_status() # If issues (eg, after 10s) -> throw an exception

    print("=== Response Info ===")
    print("Status code", response.status_code) #200, 401, 403, 500
    print("Content-type:",response.headers.get("Content-Type"))
    print("Raw bytes preview: ", response.content[:100])

    # After break, we will decode into String
    # Transform bytes into string
    decoded_text = response.content.decode("utf-8")

    print("\n === Decoded Text Preview")
    #first 200 characters of the text
    print(decoded_text[:200])

    # From the string we transform into JSON

    # Transform string into JSON
    data = json.loads(decoded_text)

    print("\n== JSON Converted ===")
    print("Type:", type(data)) #list
    print("Number of records:",len(data)) #10
    print("First user fullname: ", data[0]["name"]) # Leanne Graham

    ## Get the first user email, username
    print("First user email:", data[0]["email"])
    print("First user username:", data[0]["username"])

    # Practice to get the full address as well (Optional)

    ## Using for loop, get all the name, email and username
    for user in data:
        print(f"Name: {user["name"]} , Email: {user["email"]}, username:{user["username"]}")

    # From 0 to len(data) = 10 not including 10
    for i in range(len(data)):
        print(f"User {i+1} is {data[i]["name"]} , email: {data[i]["email"]}, username: {data[i]["username"]}")

    # Open the users_output.json in write mode using utf-8 encoding
    # Copy/dump the data in the file ensuring the unicode is enable
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data,file, ensure_ascii=False, indent=2)
        
# Test with wrong url 
except requests.RequestException as e:
    print("Request error:")
    print(e)

# KIV for the scenario 
except UnicodeDecodeError as e:
    print("Decoding error:")
    print(e)

# Test with non JSON website -> eg google.com (Can not decode the JSON)
except json.JSONDecodeError as e:
    print("JSON conversion error:")
    print(e)