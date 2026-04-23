from fastapi import FastAPI
from pydantic import BaseModel
from functools import wraps
app = FastAPI(title="Day 2 Test API")


class UserInput(BaseModel):
    username:str
    role:str

#Step 8 - Project day 2
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # kwargs here is UserInput -> Whatever that user passed in Body
        # In normal function, we use args to get the parameters -> use index of Tuple -> [0]
        # Specifically for  FastAPI , we use kwargs to get the body and path variable  information -> Dictionary ->[""]
        print(f"Received Body : {kwargs["user_input"]}")
        return func(*args, **kwargs)
    return wrapper

def transform(func): # 1 - Pass func in function name
    @wraps(func)
    def wrapper(*args, **kwargs): # 2) function wrapper
        username = kwargs["username"] #needs to be the same as variable in GET
        if username:
            kwargs["username"] = username.upper()
        return func(*args, **kwargs) # UPPERCASE THE PATH VARIABLE BEFORE THE FUNCTION IS EXECUTED
    return wrapper # 3) return wrapper

@app.get("/")
def home():
    return {"message":"Day 2 Test API is working"}

@app.post("/logging-input")
@log_action
#TODO: to add logging decorator
def log_input(user_input:UserInput):
    return {
        "message":"Request received",
        "data":user_input
    }

@app.get("/user/{username}")
@transform
def uppercase(username:str):
    return {
        "original":username.lower(),
        "transformed":username # Automatically uppercased by the decorator
    }