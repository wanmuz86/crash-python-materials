from fastapi import FastAPI
from pydantic import BaseModel

#The UserInput that will be used as body in POST API
class UserInput(BaseModel):
    name:str
    age:int

# Initialize a FastAPI server
app = FastAPI()

# API for GET method URL "/"
@app.get("/")
def home():
    return {"message":"API is running"}

@app.get("/hello")
def hello():
    return {"message":"Hello World"}

#Passing path variable in URL
# /goodbye/muzaffar
@app.get("/goodbye/{name}")
def goodbye(name:str):
    return {"message":f"Goodbye {name}"}


# Method POST, url /greet , {"name":""} needs to be passed as parameters
@app.post("/greet")
def greet(data:UserInput):
    if len(data.name.strip()) <2:
        return {"error":"Name too short"}
    if data.age <= 0:
        return {"error":"Number cannot be less than 0"}
    return {"message":f"Hello {data.name}, you are {data.age} years old"}