##############################
#                            #
#     Telstar+ Memory Map    #
#                            #
##############################

import sys

class MemoryMap:

#Virtual Variable Addresses:
#0 to 5000      -> Locals
#10000 to 15000 -> Globals
#20000 to 25000 -> Temps
#30000 to 35000 -> Constants

    #Initializes dicts for storing variables information
    def __init__(self):
        self.memory_stack = []
        self.local_vars = {}
        self.global_vars = {}
        self.temp_vars = {}
        self.const_vars = {}
        self.others = {}

    #Function that saves the memory, usually before making a call to other function or method, saving it at the memory_stack
    def saveMemory(self):
        self.memory_stack.append(self.local_vars.copy())

    #Function that returns the last instance of memory save at the memory_stack
    def loadMemory(self):
        self.local_vars = self.memory_stack.pop()

    #Reinitializes the memory, cleaning the corresponding dict
    def initMemory(self):
        self.local_vars.clear()

    #Saves data in memory, recieving as parameters the address and data to be saved.
    #Additionally, checks if data is string type and saves it as "other". If not, it checks where in the virtual addresses is it located and saves it
    #in the corresponding dict.
    def writeInMemory(self, address, data):
        if isinstance(address, str):
            self.others[address] = data
        else:
            if address <= 5000:
                self.local_vars[address] = data
            elif 10000 <= address <= 15000:
                self.global_vars[address] = data
            elif 20000 <= address <= 25000:
                self.temp_vars[address] = data
            elif 30000 <= address <= 35000:
                self.const_vars[address] = data

    #Recieves an address and returns the data stored there. If there's no data, it returns an error.
    def loadFromMemory(self, address):
        if isinstance(address, str):
            if self.others.has_key(address):
                data = self.others[address]
                return data
            else:
                print "Return error from address ", address
                sys.exit()
        elif address <= 5000:
            if self.local_vars.has_key(address):
                data = self.local_vars[address]
                return data
            else:
                print "Memory access error at address ", address
                sys.exit()
        elif 10000 <= address <= 15000:
            if self.global_vars.has_key(address):
                data = self.global_vars[address]
                return data
            else:
                print "Memory access error at address ", address
                sys.exit()
        elif 20000 <= address <= 25000:
            if self.temp_vars.has_key(address):
                data = self.temp_vars[address]
                return data
            else:
                print "Memory access error at address ", address
                sys.exit()
        elif 30000 <= address <= 35000:
            if self.const_vars.has_key(address):
                data = self.const_vars[address]
                return data
            else:
                print "Memory access error at address ", address
                sys.exit()
