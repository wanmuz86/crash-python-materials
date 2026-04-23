# To simulate global registry / class loader
# normally used in Framework

registry = []

print("Initial registry ",registry)


# We intercept the class so that by default
# When the class is created, it will auto-add itself (register) inside registry []
# This is common in framework, which auto-inialize upon startup/boot

#Create the metaclass

class AgentRegistry(type): # 1) creating the metaclass, subclass of type
    #override /intercept during 2) class creation __new___
    def __new__(cls, name, bases, dct):
        print(f"[LOG]: Creating class: {name}") #Add log upon class creation (before)
        new_class = super().__new__(cls, name, bases, dct) #calling the parent constructor (type)
        
        # Only register the subclass and not the parent class
        if name != "AgentBase":
            registry.append(new_class) # OVERRIDE BY AUTO ADD THE CLASS IN REGISTRY
        return new_class

# Create a class that is created by AgentBase metaclass 
# Observe the log come out, even before the object is created - During class creation
class AgentBase(metaclass=AgentRegistry):
    #This is the parent class, no implemtation - abstract class
    def run(self):
        raise NotImplementedError("Subluss must implement run()")

# To see the metaclass is inherits

class EmailAgent(AgentBase):
    def run(self):
        return "Sending Email..."

class ReportAgent(AgentBase):
    def run(self):
        return "Generating report...."

print("Metaclass created", AgentRegistry)
# print("Registered classes: ", registry)
for cls in registry:
    print(cls.__name__)
    #initialize and run it
    agent = cls()
    print(agent.run())