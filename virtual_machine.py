##############################
#                            #
#  Telstar+ Virtual Machine  #
#                            #
##############################

import sys
from memory_map import MemoryMap
#from available_operations import available_operations

#Variable Declarations
#current_quad: quadruple used currently for interpretation
#memory: initializes the memory map
#q_counter: counter that keeps tabs on the quadruple that is currently being executed
#jumpToRoutine_stack: stack used to keep register of the quadruple where a gotoSub was makeCuadruple
#function_buffer: current function registry
current_quad = []
memory = MemoryMap()
q_counter = 0
jumpToRoutine_stack = []
function_buffer = []

#IMPORTANT INFORMATION ABOUT MATHEMATICAL OPERATIONS
#Direct operator: The operand contains the value to be processed
#Indirect operator: The operand contains an address where the data to perform the operation is located
#Special operator: The operand contains an address, that itself contains another address (an Indirect operator)
#Default case: The normal addition between two values (for example, between two INT constants)

def addition():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #indirecto
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) + memory.loadFromMemory(op1)
    #Direct
    elif isinstance(op1, str) and op1[0] == "[" and op1[-1] == "]" and isinstance(op2, str) and op2[0] == "[" and op2[-1] == "]":
        op1 = int(op1.translate(None, "[]"))
        op2 = int(op2.translate(None, "[]"))
        temp = op1 + op2
    #op1 is Indirect, op2 is Direct
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "[" and op2[-1] == "]":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        op2 = int(op2.translate(None, "[]"))
        temp = memory.loadFromMemory(op1) + op2
    #op1 is Direct, op2 is Indirect
    elif isinstance(op1, str) and op1[0] == "[" and op1[-1] == "]" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        op1 = int(op1.translate(None, "[]"))
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = op1 + memory.loadFromMemory(op2)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op1) + memory.loadFromMemory(op2)
    #Addition of address
    elif isinstance(op1, str) and op1[0] == "[" and op1[-1] == "]":
        op1 = int(op1.translate(None, "[]"))
        temp = op1 + memory.loadFromMemory(op2)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) + memory.loadFromMemory(op1)
    #Addition of address
    elif isinstance(op2, str) and op2[0] == "[" and op2[-1] == "]":
        op2 = int(op2.translate(None, "[]"))
        temp = op2 + memory.loadFromMemory(op1)
    #Default
    else:
        temp = memory.loadFromMemory(op1) + memory.loadFromMemory(op2)
    memory.writeInMemory(res, temp)
    return q_counter + 1

def substraction():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) - memory.loadFromMemory(op1)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op1) - memory.loadFromMemory(op2)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) - memory.loadFromMemory(op1)
    #Default case
    else:
        temp = memory.loadFromMemory(op1) - memory.loadFromMemory(op2)
    memory.writeInMemory(res, temp)
    return q_counter + 1

def multiplication():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) * memory.loadFromMemory(op1)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op1) * memory.loadFromMemory(op2)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) * memory.loadFromMemory(op1)
    #Default case
    else:
        temp = memory.loadFromMemory(op1) * memory.loadFromMemory(op2)
    memory.writeInMemory(res, temp)
    return q_counter + 1

def division():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) / memory.loadFromMemory(op1)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op1) / memory.loadFromMemory(op2)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(op2) / memory.loadFromMemory(op1)
    #Default case
    else:
        temp = memory.loadFromMemory(op1) / memory.loadFromMemory(op2)
    memory.writeInMemory(res, temp)
    return q_counter + 1

#Se asigna una variable/constante/arreglo/etc.
def assignation():
    temp = current_quad[1]
    final_addr = current_quad[2]

    #op is Special
    if isinstance(temp, str) and temp[0] == "(" and temp[-1] == ")":
        indirect_addr = int(temp.translate(None, "()"))
        temp = memory.loadFromMemory(indirect_addr)
        memory.writeInMemory(final_addr, memory.loadFromMemory(temp))
    #op2 is Special
    elif isinstance(final_addr, str) and final_addr[0] == "(" and final_addr[-1] == ")":
        indirect_addr = int(final_addr.translate(None, "()"))
        final_addr = memory.loadFromMemory(indirect_addr)
        temp = memory.loadFromMemory(temp)
        memory.writeInMemory(final_addr, temp)
    #Default case
    else:
        data = memory.loadFromMemory(temp)
        memory.writeInMemory(final_addr, data)
    return q_counter + 1

def input():
    typeX = current_quad[1]
    temp = current_quad[2]

    if typeX == 1000:
        typeX = int
    elif typeX == 2000:
        typeX = float
    else:
        typeX = bool
    data = raw_input("Input: ")
    memory.writeInMemory(temp, typeX(data))
    return q_counter + 1

def greaterThan():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) > memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def greaterThanOrEqualTo():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) >= memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def lessThan():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) < memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def lessThanOrEqualTo():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) <= memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def equality():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) == memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def andOper():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) != 0 and memory.loadFromMemory(op2)!= 0:
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def orOper():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) != 0 or memory.loadFromMemory(op2) != 0:
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def notEqual():
    op1 = current_quad[1]
    op2 = current_quad[2]
    res = current_quad[3]

    #Indirect operators
    if isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")" and isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    #op1 is Special
    elif isinstance(op1, str) and op1[0] == "(" and op1[-1] == ")":
        indirect_addr = int(op1.translate(None, "()"))
        op1 = memory.loadFromMemory(indirect_addr)
    #op2 is Special
    elif isinstance(op2, str) and op2[0] == "(" and op2[-1] == ")":
        indirect_addr = int(op2.translate(None, "()"))
        op2 = memory.loadFromMemory(indirect_addr)
    if memory.loadFromMemory(op1) != memory.loadFromMemory(op2):
        temp = 1
    else:
        temp = 0
    memory.writeInMemory(res, temp)
    return q_counter + 1

def printTSP():
    address = current_quad[1]

    if isinstance(address, str) and address[0] == "(" and address[-1] == ")":
        address = int(address.translate(None, "()"))
        addr_2 = memory.loadFromMemory(address)
        dat = memory.loadFromMemory(addr_2)
    else:
        dat = memory.loadFromMemory(address)
    print dat
    return q_counter + 1

def gotoDefault():
    return current_quad[1]

def gotoFalse():
    cond = current_quad[1]

    if memory.loadFromMemory(cond) == 1:
        return q_counter + 1
    else:
        return current_quad[2]

def gotoSub():
    jumpToRoutine_stack.append(q_counter + 1)
    function_buffer.append(current_quad[1])
    return current_quad[2]

def startRout():
    memory.saveMemory()
    memory.initMemory()
    return q_counter + 1

def endRout():
    memory.initMemory()
    memory.loadMemory()
    return jumpToRoutine_stack.pop()

def retRout():
    ret_addr = current_quad[1]
    dat = memory.loadFromMemory(ret_addr)
    memory.writeInMemory(function_buffer.pop(), dat)
    return q_counter + 1

def loadParam():
    previous_memory = memory.memory_stack[-1].copy()
    temp_memory = MemoryMap()
    temp_memory.local_vars = previous_memory
    temp_memory.global_vars = memory.global_vars
    temp_memory.const_vars = memory.const_vars
    temp_memory.temp_vars = memory.temp_vars
    value = current_quad[1]
    local_addr = current_quad[2]
    dat = temp_memory.loadFromMemory(value)
    memory.writeInMemory(local_addr, dat)
    temp_memory.initMemory()
    return q_counter + 1

def arrayBoundaryVerif():
    addr = current_quad[1]
    boundary = current_quad[2]
    call_size = memory.loadFromMemory(addr)

    if 0 <= call_size < boundary:
        return q_counter + 1
    else:
        print "Error: Index out of range "
        sys.exit()

#List of available operations by the program
available_operations = {
    "+" : addition,
    "-" : substraction,
    "*" : multiplication,
    "/" : division,
    "=" : assignation,
    ">" : greaterThan,
    ">=": greaterThanOrEqualTo,
    "<" : lessThan,
    "<=" : lessThanOrEqualTo,
    "==" : equality,
    "&&" : andOper,
    "||" : orOper,
    "!=" : notEqual,
    "print" : printTSP,
    "input" : input,
    "goto" : gotoDefault,
    "gotoF" : gotoFalse,
    "goSub" : gotoSub,
    "param" : loadParam,
    "return" : retRout,
    "RET" : endRout,
    "ERA" : startRout,
    "VER" : arrayBoundaryVerif
}

class VirtualMachine:

    #Default constructor
    def __init__(self, consts, prog):
            self.const_vars = consts
            self.program = prog
            memory.const_vars = self.const_vars

    @staticmethod
    def processQuadruple(quad):
        global current_quad
        current_quad = quad
        action = quad[0]
        return available_operations[action]()

    def runProgram(self):
        global q_counter
        print "Executing program..."
        while q_counter < len(self.program):
            q_counter = self.processQuadruple(self.program[q_counter])
