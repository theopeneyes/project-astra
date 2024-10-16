# This file contains the event listener addition class
#TODO: Implement event listener to logs things into a db 
# for help read this link: https://stackoverflow.com/questionsquestions/70982565/how-do-i-make-an-event-listener-with-decorators-in-python/74679391#74679391

class Event:
    def __init__(self):
        # Initialise a list of listeners
        self.__listeners = []
    
    # Define a getter for the 'on' property which returns the decorator.
    @property
    def on(self):
        # A declorator to run addListener on the input function.
        def wrapper(func):
            self.addListener(func)
            return func
        return wrapper
    
    # Add and remove functions from the list of listeners.
    def addListener(self,func):
        if func in self.__listeners: return
        self.__listeners.append(func)
    
    def removeListener(self,func):
        if func not in self.__listeners: return
        self.__listeners.remove(func)
    
    # Trigger events.
    def trigger(self,args = None):
        # Run all the functions that are saved.
        if args is None:
            args = []
        for func in self.__listeners: func(*args)