import time # to store the time [because we limit within 1 minutes]
from functools import wraps # to create decorator and avoid the metadata bug


#decorator with shared variable
# max_calls = how many calls = 1000
# window_seconds = per how long 60x60x24 (1 day)
def rate_limit(max_calls, window_seconds):
    call_timestamps = [] #shared variables - we store all the timestamps of the API call
 
    
    def decorator(func):

        def wrapper(*args, **kwargs):
            
            current_time = time.time() # get the current time
            #check all the times, to ensure that we only keep the last 60s
            valid_calls = []
            for timestamp in call_timestamps:

                # change the formula, to be dynamic, not hardcoded to 60s
                if current_time - timestamp < window_seconds:
                    valid_calls.append(timestamp) # only save the timestamp that is less than 60s ago

            call_timestamps.clear()
            call_timestamps.extend(valid_calls) #update with the recent api call timetamps

            print(f"[LOG]: Request timestamp: {current_time:.2f}") # formated at 2 decimal point

            #if the call exceed the max allowed limit, eg: 3
            # it will raise an exception , the call will be blocked
            if len(call_timestamps) >= max_calls:
                raise Exception(f"Rate limit exceeded , only {max_calls} calls allowed per minute")

            call_timestamps.append(current_time)

            return func(*args, **kwargs)        

        return wrapper
    return decorator
    

#Imagine this an API call (today's project)

# We will set the number of time this function can be called per minute
# throttle Request
# decorator

@rate_limit(max_calls=5, window_seconds=10)
def send_request():
    print("Request processed successfully")

for i in range(6):
    try:
        print(f"\n Attempt {i+1}")
        send_request()
    except Exception as e:
        print("[Error]", e)
    time.sleep(2) #wait for 1s, check the timing in log as well

# send_request()
# send_request()
# send_request()
# send_request() #this request will fail as it has exceed the number of request per minute