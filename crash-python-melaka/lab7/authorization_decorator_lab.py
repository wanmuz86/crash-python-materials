from functools import wraps
current_user = {
    "username":"wan",
    "role":"user"
}

# Creating a custom exception
# REMINDER : inherits (Exception)
class AuthorizationError(Exception):
    pass

#decorator with argument
def require_role(required_role):

    def decorator(func): # rule 1
        @wraps(func) # to fix the metadata issue
        def wrapper(*args, **kwargs): #rule 2
            # func.__name__ can be only retrieved once we have done the @wraps(func)
            print(f"[LOG] User '{current_user['username']} attempting to access '{func.__name__}'")

            #we read from the hardcoded value, but later it is coming from API 
            if current_user["role"] != required_role:
                print("[LOG] Access denied")
                raise AuthorizationError(
                    f"User '{current_user['username']}' does not have the required role '{current_user['role']}'")
            print("[LOG] Access granted")
            return func(*args, **kwargs) #execute the wrapped function

        return wrapper #rule 2
    return decorator


# We will protect this function can only be called by admin
@require_role("admin")
def delete_user():
    print("User deleted successfully")

@require_role("admin")
def create_user(): #demo on how one decorator can be called in multiple function
    print("User created successfully")

try:
    delete_user()
    create_user()
except AuthorizationError as e:
    print("[ERROR]",e)