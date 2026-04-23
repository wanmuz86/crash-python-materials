from fastapi import FastAPI, HTTPException
from dtos.user_input import UserInput
from models.user import User
from functools import wraps

app = FastAPI(title="Secure Data API")

# this is to simulate the DB
# for this exercise all th user will be stored here
# in production this will be DB Connection
users_db = []


# Decorators
#Username validation (step 7)
def validate_unique_username(func):
    @wraps(func)
    # pass the body as wrapper parameter (we can also do like this in the test)
    def wrapper(user_input,*args, **kwargs):
        # for each SAVED user in the temporary DB
        for user in users_db:
            # verify if the username already exists
            if user["username"] == user_input.username:
                # throw 400 error
                raise HTTPException(status_code=400, detail="Username already exists")
        #finished checking
        return func(user_input, *args, **kwargs)
    return wrapper

#similar to our day-2 test notes
def log_action(func):
   @wraps(func)
   def wrapper(*args, **kwargs):
       print(f"[LOG] Executing endpoint: {func.__name__}")
       return func(*args, **kwargs)
   return wrapper

#decorator with argument
# We will protect some of the route for a particular user role, eg: admin, manager only
def requires_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # For simulation only we will get the role from parameters
            # IN REALITY WE GET IT FROM THE TOKEN PASSED THROUGH HEADER , eg: JWT
            # For testing, you will call : hello?current_role=admin
            current_role = kwargs.get("current_role")
            if current_role != required_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"Access denied. Required role: {required_role}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
    

@app.get("/")
@log_action
def home():
    return {"message":"Secure Data API is running"}

@app.post("/register")
@log_action
@validate_unique_username
def register_user(user_input:UserInput):
    try:
        user = User(
            username=user_input.username,
            email=user_input.email,
            age=user_input.age,
            role=user_input.role
        )
        users_db.append(user.to_dict())
        return {
            "message":"User successfully registered",
            "user":user.to_dict()
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# users?current_role=admin
#users?current_role=user => 403 (Unauthorized)
# query parameters ?current_role
@app.get("/users")
@log_action
@requires_role("admin")
def list_users(current_role:str):
    return {
        "total_users":len(users_db),
        "users":users_db
    }