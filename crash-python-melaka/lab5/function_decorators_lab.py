from functools import wraps

#Manually create the wrapper
#func is passed as parameter here
def simple_decorator(func):
    #wrapper define the behaviour to intercept the func 
    def wrapper(*args, **kwargs): # COMPULSARY wrapper name
        print("Before the function runs")
        print(f"Arguments passed are {args}")

        # add return tu support function with return
        result = func(*args, **kwargs) # Executing the function
 
        print("After the function runs")
        return result
    
    return wrapper # COMPULSARY needs to be returned


#Used the defined decorator with @simple_decorator
# Function that we want to wrap
@simple_decorator
def greet(name):
    print(f"Hello {name}, welcome to Python decorators!")

greet("Wan")



# Sample code of a logger
def log_call(func):
    # To retrieve the function name and docs __name__ and __doc__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling function: {func.__name__}")
        #args is the arguments passed one or more *args => can be 0 or more
        print(f"[LOG]:Args: {args}, Kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] Result: {result}")
        return result
    return wrapper

# Function with return
@log_call
def multiply(a,b):
    return a*b

value = multiply(4,6)
print("-- Final logger-- result")
print("Final value:", value)
print("Function name:", multiply.__name__)
print("Docstring:", multiply.__doc__)



def uppercase_output(func):
    @wraps(func) # to ensure the metadata is not lost
    def wrapper(*args, **kwargs):
        #this needs to be string then only we uppercase it
        result = func(*args, **kwargs)
        if type(result) is str :
            return result.upper()
        return result
    return wrapper

# TO CREATE THE DECORATOR THAT WILL INTERCEPT THE FUNCTION AND UPPERCASE IT
@uppercase_output
def say_hello():
    return "hello world"

print(say_hello())