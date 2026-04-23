from functools import wraps
import unicodedata
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Mini Agentic AI Framework")

# User Input - Text instruction for the AI
# eg: clean the data "Cafe a la francaise", there is an error with server at the moment, 
# give me the report, fix the login issue urgently
class UserInput(BaseModel):
   text: str


agent_registry = {}

# Meta class

class AgentRegistry(type):
    #Override the __new__ method
    def __new__(cls, name, bases,dct):
        new_class = super().__new__(cls, name, bases, dct)

        #skip the base class
        if name != "BaseAgent":
            #automatically registered all class  that 
            # inherits the metaclass inside registry
            agent_registry[name] = new_class
        
        return new_class

# Parent class that needs to be implemented
class BaseAgent(metaclass=AgentRegistry):
    #validation
    def validate(self,data):
        raise NotImplementedError("Subclasses must implement validate()")
    
    def execute(self, data):
        raise NotImplementedError("Subclasses must implement execute()")
    
    # The implementaion is defined here it is not an sbtract class
    def log(self, message):
        print(f"[AGENT LOG] {self.__class__.__name__}: {message}")

#Decorator

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Starting: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] finished:{func.__name__}")
        return result
    return wrapper

def validate_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # retrieve the arguments to perform validation
        data = args[1] if len(args) > 1 else None

        #String validation
        if not isinstance(data,str):
            raise ValueError("Input must be a string")
        
        #Not empty validation
        if not data.strip():
            raise ValueError("Input cannot be empty")
        
        return func(*args, **kwargs)
    
    return wrapper

#Retries a failed function in case of unstable AI steps
def retry(max_attempts=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error  = None

            for attempt in range(1, max_attempts+1):
                try:
                    print(f"[RETRY] Attempt {attempt} for {func.__name__}")
                    return func(*args,**kwargs)
                except Exception as e:
                    print(f"[RETRY] failed attempt {attempt}: {e}")
                    last_error = e
            raise last_error
        return wrapper
    return decorator

#unicode relate

def clean_unicode_text(text:str)-> str:
    cleaned = "".join(text.strip().split())
    normalized = unicodedata.normalize("NFC", cleaned)
    return normalized

#Simulate AI thinking by detecting the keyword
# When create real agentic project, this will be performed by OpenAI and the library (langchain)
def mock_ai_call(task: str, text: str):
   text_lower = text.lower()
 
   if task == "classify": #classification taskt
       if "error" in text_lower or "urgent" or "critical" in text_lower:
           return "high_priority" # instruction with urgen and error will be given to high priority agent
       elif "clean" in text_lower or "data" in text_lower:
           return "data_task" # instruction with clean will be given to data_task agent
       else:
           return "general" # otherwise it will be give to general agent"

   if task == "decision":  #decision task
       if "high_priority" in text_lower:
           return "Escalate to admin"
       elif "data_task" in text_lower:
           return "Send to data team"
       else:
           return "Standard processing"

   return "unknown"

# Create the three agents
# All the agents will inherit the BaseAgent that is created by a Metaclass (auto registered)
# Data Cleaning 
class DataCleaningAgent(BaseAgent):
    def validate(self, data):
        # Validation for this agent
        return isinstance(data, str) and len(data.strip()) > 0
    
    @log_execution
    @validate_input
    def execute(self,data):
        self.log("Cleaning Unicode text")
        return clean_unicode_text(data)


# TextClassficiation

class TextClassificationAgent(BaseAgent):
    #data is data passed by API (later)
    def validate(self, data):
        return isinstance(data,str) and len(data.strip()) > 0
    
    @retry(max_attempts=2)
    @log_execution
    @validate_input
    def execute(self, data):
        self.log("Classifiying data")
        return mock_ai_call("classify", data)


#DecisionAgent
class DecisionAgent(BaseAgent):
    def validate(self,data):
        return isinstance(data,str) and len(data.strip())> 0
    
    @retry(max_attempts=2)
    @log_execution
    @validate_input
    def execute(self, data):
        self.log("Making decision")
        return mock_ai_call("decision", data)


#Create the orchestrator class
# Orchestrator -> The class that will manage the agent / distribute the task to the agent
# We will see in detail in Agentic AI course

class AgentOrchestrator:
    # initializer/constructor, create a logs lost
    def __init__(self):
        self.logs= []
    
    def log(self,message):
        print(f"[ORCHESTRATOR] {message}")
        self.logs.append(message)
    
    def get_agent(self, agent_name):
        #Return the agent by given name from registry
        agent_class = agent_registry.get(agent_name)
        if not agent_class:
            raise ValueError(f"Agent not found: {agent_name}")
        return agent_class()
    
    def run_workflow(self, user_input):
        try:
            self.log("Starting worklow")

            # Clean the user input from API , task by DataCleaningAgent
            cleaner = self.get_agent("DataCleaningAgent")
            cleaned_text = cleaner.execute(user_input)
            self.log(f"Cleaned text: {cleaned_text}")

            # In Agentic AI, this is What to do
            classifier = self.get_agent("TextClassificationAgent")
             #Check with mock_ai code
            classification = classifier.execute(cleaned_text) # decide, high_priotiy, general or data_task
            self.log(f"Classification:{classification}")

            #In agentic AI, this is execute based on decision
            decider = self.get_agent("DecisionAgent")
            #Check with mock_ai code
            decision = decider.execute(classification) # perform between - high_priory, ecalate , data team or standard
            self.log(f"Decision: {decision}")

            self.log("Workflow completed successfully")

            return {
                "input":user_input, 
                "cleaned_text":cleaned_text,
                "classification":classification,
                "decision":decision,
                "logs":self.logs
            }



        except Exception as e:
            self.log(f"Workflow failed: {e}")
            raise

@app.get("/")
def home():
   return {"message": "Mini Agentic AI Framework is running"}

#Retrieved all the registered agents - That is auto created by metaclass
@app.get("/agents")
def list_agents():
   return {"registered_agents": list(agent_registry.keys())}

# Process the instruction given in body - "AI Instruction"
@app.post("/process")
def process_text(payload: UserInput):
   orchestrator = AgentOrchestrator()

   try:
       result = orchestrator.run_workflow(payload.text)
       return result
   except Exception as e:
       raise HTTPException(status_code=400, detail=str(e))
