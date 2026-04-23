# Our Entity
# IN REALITY THIS WILL BE LINKED TO DATABASE

class User:
    # Define the property (private) and constructor 
    def __init__(self, username:str, email:str, age:int, role:str):
        self.username = username
        self.email = email
        self.age = age
        self.role = role

    # define the getter and setter using @property
    # The validation will happen here (setter)
    # if any property needs to be transformed can be done on getter
    @property
    def username(self):
        return self._username #no transformation

    @username.setter
    def username(self,value):
        #Overriding the default setter by adding validation
        #perform validation before saving
        if not value or len(value.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long")
        self._username = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    #Overriding the default setter by adding validation
    #perform validation before saving
    def email(self,value):
        if "@" not in value: # improve by using regex
            raise ValueError("Invalid email address")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 18:
            raise ValueError("User must be at least 18 years old")
        self._age = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        allowed_roles = ["admin", "user"]
        if value not in allowed_roles:
            raise ValueError("Role must be 'admin' or 'user'")
        self._role = value

    #what is the different between self._username and self.username?
    # without the _ i am calling the @property / getter/setter
    # with _ i'm accessing/modifying  the variable directly
    def to_dict(self):
        return {
            "username":self.username,
            "email":self.email,
            "age":self.age,
            "role":self.role
        }