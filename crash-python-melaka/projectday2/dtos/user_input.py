from pydantic import BaseModel

#request models
#structure of the JSON for POST request

class UserInput(BaseModel):
    username:str
    email:str
    age:int
    role:str