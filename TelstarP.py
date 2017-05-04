##############################
#                            #
#  Telstar+ Lex and Grammar  #
#                            #
##############################

import sys
import ply.lex as lex
import ply.yacc as yacc
from semantic_cube import matchOp
from virtual_machine import VirtualMachine

#---------------------------------------------------------------------#
#                            Telstar+ Lex                             #
#---------------------------------------------------------------------#

reserved = {
   #'program' : 'PROGRAM',
   'int' : 'TYPE_INT',
   'float' : 'TYPE_FLOAT',
   'boolean' : 'TYPE_BOOLEAN',
   'void' : 'TYPE_VOID',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'do' : 'DO',
   'return' : 'RETURN',
   'print' : 'PRINT',
   'input' : 'INPUT',
   'main' : 'MAIN',
   #'Telstar+' : 'TSP'
}

tokens = [
    'ID',
    'INT',
    'FLOAT',
    'BOOLEAN',
    'END_LINE',
    'COMMA',
    'AS_OPERATOR',
    'MD_OPERATOR',
    'LOGIC_OPERATOR',
    'AO_OPERATOR',
    'ASSIGN',
    'L_BRACKET',
    'R_BRACKET',
    'L_PAR',
    'R_PAR',
    'BRACES'] + list(reserved.values())

t_ignore = ' \t\n'

#Identifiers
def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9]*'
    token.type = reserved.get(token.value,'ID')
    return token

#Data types
def t_INT(token):
    r'[0-9]+'
    token.value = int(token.value)
    return token

def t_FLOAT(token):
    r'[0-9]*\.[0-9]+'
    token.value = float(token.value)
    return token

def t_BOOLEAN(token):
    r'[0-1]'
    return token

#Separators
def t_END_LINE(token):
    r'\;'
    return token

def t_COMMA(token):
    r'\,'
    return token

#Operators
def t_AS_OPERATOR(token):
    r'\+|\-'
    return token

def t_MD_OPERATOR(token):
    r'\*|/'
    return token

def t_LOGIC_OPERATOR(token):
    r'>|<|>=|<=|==|!='
    return token

def t_AO_OPERATOR(token):
    r'&&|\|\|'
    return token

def t_ASSIGN(token):
    r'='
    return token

#Special characters
def t_L_BRACKET(token):
    r'\['
    return token

def t_R_BRACKET(token):
    r'\]'
    return token

def t_L_PAR(token):
    r'\('
    return token

def t_R_PAR(token):
    r'\)'
    return token

def t_BRACES(token):
    r'\{|\}'
    return token

#Syntax Error
def t_error(t):
    print 'Syntax Error: Invalid character ', t.value[0]
    sys.exit()

#---------------------------------------------------------------------#
#                         Telstar+ Aux Functions                      #
#---------------------------------------------------------------------#
#Addresses Listing
#
#Local Addresses:
#0 a 1000 -> int
#1000 a 2000 -> float
#2000 a 3000 -> boolean
localAddr_int = 0
localAddr_float = 1000
localAddr_bool = 2000

#Global Addresses:
#10000 a 11000 -> int
#11000 a 12000 -> float
#12000 a 13000 -> boolean
globalAddr_int = 10000
globalAddr_float = 11000
globalAddr_bool = 12000

#Temporal Addresses:
#20000 a 21000 -> int
#21000 a 22000 -> float
#22000 a 23000 -> boolean
tempAddr_int = 20000
tempAddr_float = 21000
tempAddr_bool = 22000

#Constant Addresses:
#30000 a 31000 -> int
#31000 a 32000 -> float
#32000 a 33000 -> boolean
constAddr_int = 30000
constAddr_float = 31000
constAddr_bool = 32000

#Table and Aux declarations
#procs -> Procedures table
#variables -> Variables table
#constants -> Constants table
#vars_sizeOf -> Size of variables table
#procs_identifier -> Type of procedures table
#vars_identifier -> Type of variables table
#params_buffer -> Function parameters buffer
procs = { }
variables = { }
constants = { }
vars_sizeOf = { }
procs_identifier = { }
vars_identifier = []
params_buffer = []

#Quadruples Generation
#quad_buffer -> Quadruples buffer
#quadruples -> Quadruple manager
#temp_count -> Temporal counter
#current_quad -> The currently processed quadruple
#main_quad -> Quadruples in the Main part of the program
#param_num -> Number of parameters sent with the quadruples
#goto_stack -> Manages the jumps
#initQuad_stack -> Generates a stack of quadruples for a function
#functSize_stack -> Stores the size of the functions
quad_buffer = []
quadruples = [['goto', -1]]
temp_count = 1
current_quad = 1
main_quad = 0
param_num = 0
goto_stack = []
initQuad_stack = []
functSize_stack = []

#Possible Operations Buffers
AddSub_Ops = []
MultDiv_Ops = []
AndOr_Ops = []
logic_Ops = []


#Functions for checking if the variable exists in the given local and the global scope
def scopeVarVerif(var, scope):
    if var[0] in variables[scope]:
        type1 = typeVar(variables[scope][var[0]])
        type2 = opTypeConverter(var[1], scope)
        if dataValidation(type1 / 1000, type2 / 1000, 6, "assignation"):
            return True
    elif 'global' in variables.keys():
        if var[0] in variables['global']:
            type1 = typeVar(variables['global'][var[0]])
            type2 = opTypeConverter(var[1], 'global')
            if dataValidation(type1 / 1000, type2 / 1000, 6, "assignation"):
                return True
        else:
            return False
    else:
        return False

#Recieves a variable and its scope and returns the variable type
def typeVarName(var, scope):
    if var[0] in variables[scope]:
        return typeVar(variables[scope][var[0]])
    elif 'global' in variables.keys():
        if var[0] in variables['global']:
            return typeVar(variables['global'][var[0]])

#Recieves two operands and an operator, and calls matchOp from the semantic cube to get the validity of the operation
def dataValidation(op1, op2, operator, message):
    if matchOp(op1, op2, operator) == -1:
        print "Error: Not compatible types in operation ", message
        sys.exit()
    else:
        return matchOp(op1, op2, operator) * 1000

#Calculates the local address of a variable given the type, recieving also the variable size
def localAddrCalculator(typeX, size):
    if typeX == 'int':
        global localAddr_int
        localAddr_int += size
        return localAddr_int - size
    elif typeX == 'float':
        global localAddr_float
        localAddr_float += size
        return localAddr_float - size
    else:
        global localAddr_bool
        localAddr_bool += size
        return localAddr_bool - size

#Calculates the global address of a variable given the type, recieving also the variable size
def globalAddrCalculator(typeX, size):
    if typeX == 'int':
        global globalAddr_int
        globalAddr_int += size
        return globalAddr_int - size
    elif typeX == 'float':
        global globalAddr_float
        globalAddr_float += size
        return globalAddr_float - size
    else:
        global globalAddr_bool
        globalAddr_bool += size
        return globalAddr_bool - size

#Calculates the temporal address of a variable given the type, recieving also the variable size
def tempAddrCalculator(typeX):
    if typeX == 'int':
        global tempAddr_int
        tempAddr_int += 1
        return tempAddr_int - 1
    elif typeX == 'float':
        global tempAddr_float
        tempAddr_float += 1
        return tempAddr_float - 1
    else:
        global tempAddr_bool
        tempAddr_bool += 1
        return tempAddr_bool - 1

#Calculates the constant address of a variable given the type, recieving also the variable size
def constAddrCalculator(typeX):
    if typeX == 'int':
        global constAddr_int
        constAddr_int += 1
        return constAddr_int - 1
    elif typeX == 'float':
        global constAddr_float
        constAddr_float += 1
        return constAddr_float - 1
    else:
        global constAddr_bool
        constAddr_bool += 1
        return constAddr_bool - 1

#Recieves an address and returns the type of the variable stored in said address
def typeVar(address):
    if address < 1000 or 10000 <= address < 11000 or 20000 <= address < 21000:
        return 1000
    elif 1000 <= address < 2000 or 11000 <= address < 12000 or 21000 <= address < 22000:
        return 2000
    else:
        return 3000

#Recieves the name of a variable and returns the type
def typeName(typeIDX):
    if typeIDX == 1000:
        return 'int'
    elif typeIDX == 2000:
        return 'float'
    elif typeIDX == 3000:
        return 'boolean'
    else:
        return 'void'

#Recieves the type as paramater and returns the corresponding key for that data type
def typeID(typeX):
    if typeX == 'int':
        return 1000
    elif typeX == 'float':
        return 2000
    elif typeX == 'boolean':
        return 3000
    elif typeX == 'void':
        return 4000

#Recieves an operator and returns its corresponding semantic cube key
def operID(opr):
    if opr == "+" or opr == "-":
        return 1
    elif opr == "*" or opr == "/":
        return 2
    elif opr == "&&" or opr == "||":
        return 3
    elif opr == "<" or opr == ">" or opr == "<=" or opr == ">=":
        return 4
    elif opr == "==" or opr == "!=":
        return 5
    elif opr == "=":
        return 6

#Function that interprets the chain of operations stored in dictionaries to determine the type of an operations
#Recieves a chain of operations and the scope where it was created, returning the type the result should be
def opTypeConverter(d, scope):
    if isinstance(d, int): #It's already a type
        return d
    elif isinstance(d, list): #It's a list of operations
        print d
    elif isinstance(d, dict): #There's another variable operating
        var1 = d.keys()[0]
        if var1 in variables[scope].keys(): #Looks for an existing variable in the scope
            type1 = typeVar(variables[scope][var1])
            return opTypeAux(d[var1], type1, scope)
        elif (var1 in procs.keys() and d[var1].has_key(9999)) or (var1 == -1 and d[var1].has_key(9999)): #9999 means it's a function
            if d[var1][9999] is not None:
                called_args = d[var1][9999]
                func_args = list(procs[var1]['params'].values())
                if len(called_args) != len(func_args):
                    print "Error: Number of arguments in function ", var1
                    sys.exit()
                for arg in called_args:
                    if isinstance(arg, dict): #if arg is a variable, check that it's declared
                        if scopeVarVerif((arg.keys()[0], arg), scope):
                            arg = typeVarName(arg.keys()[0], scope)
                        else:
                            print "Error: Undeclared argument ", arg.keys()[0]
                            sys.exit()
                    for param in func_args: #Verify compatibility between expected and given arguments
                        if dataValidation(arg / 1000, typeVar(param) / 1000, 6, "assignation"):
                            func_args.remove(param)
                            break
                if len(func_args) == 0:
                    return procs[var1]['type']
                else:
                    print "Error: Arguments not consistent in function ", var1
                    sys.exit()
            else:
                if len(procs[var1]['params'].keys()) == 0:
                    return procs[var1]['type']
                else:
                    print "Error: Expected arguments in function ",  var1
                    sys.exit()
        elif scope != "main" and procs[scope].has_key('params'):
            if var1 in procs[scope]['params']:
                type1 = typeVar(procs[scope]['params'][var1])
                return opTypeAux(d[var1], type1, scope)
        else:
            print "Error: Undeclared variable or function ", var1
            sys.exit()

#Aux function that recieves a list of operations and an initial type of variable or function and its scope, returning the type of the list of operations
def opTypeAux(oper_list, initial_type, scope):
    type1 = initial_type
    for op in oper_list:
        operation = op[0]
        if isinstance(op[1], dict):
            type2 = opTypeConverter(op[1], scope)
        else:
            type2 = op[1]
        type1 = dataValidation(type1 / 1000, type2 / 1000, operation, "assignation")
    return type1

#Generates and adds a quadruple to the quadruple list. Recieves a list with the action necessary to generate said quadruple.
def quadGenerator(action):
    global quad_buffer
    global temp_count
    global current_quad
    opr = action.pop()
    if opr == "goto":
        quad = [opr, -1]
        goto_stack.append(current_quad)
        quadruples.append(quad)
        current_quad += 1
    elif opr == "ERA":
        functSize_stack.append(current_quad)
        quad = [opr, action.pop()]
        quadruples.append(quad)
        current_quad += 1
    elif opr == "goSub":
        quad = [opr, action.pop(), -1]
        quadruples.append(quad)
        current_quad += 1
    elif opr == "param":
        global param_num
        param = quad_buffer.pop()
        num_par = action.pop() + str(param_num)
        quad = [opr, param, num_par]
        quadruples.append(quad)
        param_num -= 1
        current_quad += 1
    elif opr == "VER":
        var_name = action.pop()
        offset = action.pop()
        quad = [opr, offset, var_name]
        quadruples.append(quad)
        current_quad += 1
    elif len(quad_buffer) > 0:
        op1 = quad_buffer.pop()
        temp = "-0TMP" + str(temp_count) #Temporal identifier
        if opr == "=":
            if len(quad_buffer) > 0:
                op2 = quad_buffer.pop()
                quad = [opr, op2, op1]
        elif opr == "print":
            quad = [opr, op1]
        elif opr == "input":
            quad = [opr, typeID(op1), temp]
            quad_buffer.append(temp)
            temp_count += 1
        elif opr == "gotoF":
            quad = [opr, op1, -1] #-1: Quad Complete
            goto_stack.append(current_quad)
        else:
            if len(quad_buffer) > 0:
                op2 = quad_buffer.pop()
                quad = [opr, op2, op1, temp]
                quad_buffer.append(temp)
                temp_count += 1
        quadruples.append(quad)
        current_quad += 1

#Adds the function size to the ERA quadruples
def functSizeComp():
     while len(functSize_stack) > 0:
         goto_fsc = functSize_stack.pop()
         quad = quadruples[goto_fsc]
         function = quad[-1]
         if isinstance(function, basestring):
             size = procs[function]['size']
             quad[-1] = size
             quadruples[goto_fsc] = quad

#Manages the jump to main
def gotoMainComp(init):
    first_quad = quadruples[0]
    if first_quad[-1] == -1:
        first_quad[-1] = init
        quadruples[0] = first_quad

#Manages missing jumps to subroutines
def gotoSubComp():
    for quad in quadruples:
        if quad[0] == "goSub" and quad[-1] == -1:
            goto_fsc = quad[1]
            init_addr = procs[goto_fsc]['start']
            quad[-1] = init_addr
            idx = quadruples.index(quad)
            quadruples[idx] = quad

#Generates temporal addresses for the quadruples that require them
def tempQuadAddr():
    assigned_temp = {}
    for quad in list(quadruples):
        i = 1
        while i < len(quad):
            temp = quad[i]
            if isinstance(temp, str) and "-0TMP" in temp: #Checks for the temporal identifier
                par_lim = False
                quad_lim = False
                if temp[0] == "(" and temp[-1] == ")":
                    par_lim = True
                    temp = temp.translate(None, "()")
                if temp[0] == "[" and temp[-1] == "]":
                    quad_lim = True
                    temp = temp.translate(None, "[]")
                if assigned_temp.has_key(temp): #If the temp was already assigned, the address is brought
                    temp = assigned_temp[temp]
                else:
                    res = matchOp(typeVar(quad[1]), typeVar(quad[2]), operID(quad[0])) #Gets type to calculate a correct corresponding address
                    temp_addr = tempAddrCalculator(res * 1000)
                    assigned_temp[temp] = temp_addr
                    temp = temp_addr
                idx = quadruples.index(quad)
                if par_lim:
                    quad[i] = "(" + str(temp) + ")"
                elif quad_lim:
                    quad[i] = "[" + str(temp) + "]"
                else:
                    quad[i] = temp
                quadruples[idx] = quad
            i += 1

#Obtains the address of a variable based on the quadruple number, recieving the variable name and its corresponding quadruple
def retVarAddr(var, quad_num):
    near = 999999999 #Where it will start looking
    main_start = quadruples[0][1]
    scope_var = ""
    for scope in variables.keys(): #Checks for a close function
        if scope is not "main" and scope is not "global":
            start = procs[scope]['start']
            if start <= quad_num and quad_num - start < near:
                scope_var = scope
                near = quad_num - start
    if near == 999999999 or (quad_num >= main_start and quad_num - main_start < near): #Checks the main scope
        scope_var = 'main'
    array = False
    quad_del = False
    if var[0] == "(" and var[-1] == ")":
        array = True
        var = var.translate(None, "[]")
    if var[0] == "[" and var[-1] == "]":
        array = True
        quad_del = True
        var = var.translate(None, "[]")
    if scope_var is not "main" and scope_var is not "global" and var in procs[scope_var]['params'].keys():
        if array:
            if quad_del:
                return "[" + str(procs[scope_var]['params'][var]) + "]"
            else:
                return "(" + str(procs[scope_var]['params'][var]) + ")"
        else:
            return procs[scope_var]['params'][var]
    elif scope_var in variables.keys():
        if var in variables[scope_var].keys():
            if array:
                if quad_del:
                    return "[" + str(variables[scope_var][var]) + "]"
                else:
                    return "(" + str(variables[scope_var][var]) + ")"
            else:
                return variables[scope_var][var]
        else:
            if variables.has_key('global') and var in variables['global'].keys():
                if array:
                    if quad_del:
                        return "[" + str(variables['global'][var]) + "]"
                    else:
                        return "(" + str(variables['global'][var]) + ")"
                else:
                    return variables['global'][var]
            else:
                if array:
                    if quad_del:
                        return "[" + var + "]"
                    else:
                        return "(" + var + ")"
                else:
                    if var in procs.keys() or "-" in var:
                        return var
                    else:
                        print "Error: Undeclared ID", var #Not found
                        sys.exit()

#Returns variable size from its quadruple and scope. Recieves the vaiable ID and the quadruple number.
def retvar_size(var, quad_num):
    near = 999999999
    main_start = quadruples[0][1]
    scope_var = ""
    for scope in variables.keys():
        if scope is not "main" and scope is not "global":
            start = procs[scope]['start']
            if start <= quad_num and quad_num - start < near:
                scope_var = scope
                near = quad_num - start
    if near == 999999999 or (quad_num >= main_start and quad_num - main_start < near):
        scope_var = 'main'
    if vars_sizeOf.has_key(scope_var):
        if vars_sizeOf[scope_var].has_key(var):
            return vars_sizeOf[scope_var][var]

#Translates variable IDs to their addresses
def addrQuadTranslator():
    i = 0
    for quad in quadruples:
        j = 1
        while j < len(quad):
            if isinstance(quad[j], str) and "-0TMP" not in quad[j] and quad[0] is not "goSub" and quad[j] is not "param" and quad[0] is not "VER":
                quad[j] = retVarAddr(quad[j], i)
            j += 1
        quadruples[i] = quad
        i += 1

#Manages the array verification quadruples (VER)
def arrayQuadVerif():
    i = 0
    for quad in quadruples:
        if quad[0] == "VER":
            if isinstance(quad[2], str):
                quad[2] = retvar_size(quad[2], i)
            if isinstance(quad[1], str):
                quad[1] = retVarAddr(quad[1], i)
        quadruples[i] = quad
        i += 1

#Assigns parameters during function calls in the expected order.
def paramAssign():
    i = 0
    for quad in quadruples:
        if quad[0] == "param":
            keys = quad[2].split("-")
            function_name = keys[0]
            param_no = int(keys[1])
            param_name = procs[function_name]['param_order']
            param_name = param_name[param_no]
            param_add = procs[function_name]['params'][param_name]
            quad[2] = param_add
            quadruples[i] = quad
        i += 1

#---------------------------------------------------------------------#
#                            Telstar+ Grammar                         #
#---------------------------------------------------------------------#

#PROGRAM
def p_program(p):
    '''program : program_2 inicioMain BRACES code_statute BRACES'''
    #Declared vars
    main_variables = { }
    main_Vsizes = { }
    if p[4] is not None and p[4].has_key('temp_vars'):
        local_vars = p[4]['temp_vars'].copy()
        del p[4]['temp_vars']
        for var_name in local_vars.keys():
            code = local_vars[var_name]
            atts = code.split("-")
            addr = int(atts[0])
            var_size = int(atts[1])
            main_variables.update({var_name : addr})
            main_Vsizes.update({var_name : var_size})
    variables['main'] = main_variables
    vars_sizeOf['main'] = main_Vsizes
    scope = 'main' #For variables called at the scope
    if p[4] is not None and p[4].has_key('call'):
        if scope in variables.keys(): #Looks in the scope and globally
            for key in list(p[4]['call']):
                if scopeVarVerif(key, scope):
                    p[4]['call'].remove(key)
        for key in list(p[4]['call']): #For void functions
            if key[0] == -1:
                if opTypeConverter(key[1], 'main'):
                    p[4]['call'].remove(key)
        if len(p[4]['call']) > 0:
            print "Error: Undeclared variable ", p[4]['call'][0][0], " at scope ", scope
            sys.exit()
    for key in list(procs_identifier.keys()):
        if key in procs.keys() and procs[key]['type'] == procs_identifier[key]:
            del procs_identifier[key]
        else:
            print "Error: Undeclared function ", key, " type ", typeName(procs_identifier[key])
            sys.exit()
    functSizeComp()
    gotoMainComp(p[2]) #goto Main
    gotoSubComp() #Adds jumps to subroutines
    arrayQuadVerif() #Array verification
    addrQuadTranslator() #Adds missing addresses to quads
    tempQuadAddr() #Adds temp addresses
    paramAssign() #Adds params addresses
    print "Succesful program build..."

#MAIN initialization with its corresponding goto
def p_inicioMain(p):
    '''inicioMain : MAIN'''
    p[0] = current_quad

#Variables globales y funciones
def p_program_2(p):
    '''program_2 : type ID program_aux program_2
                   | '''
    global main_quad
    main_quad = current_quad
    if len(p) > 3:
        if p[3] is not None:
            if p[3].has_key('var'): #Global var declaration
                if p[3]['var'] == 'var':
                    v_size = 1
                else:
                    v_size = p[3]['var']
                del p[3]['var']
                data_addr = globalAddrCalculator(p[1], v_size)
                for key in p[3]:
                    if p[3][key] == 'var':
                        v_size = 1
                    else:
                        v_size = p[3][key]
                    p[3][key] = globalAddrCalculator(p[1], v_size)
                temp_vars = {p[2] : data_addr}
                temp_vars.update(p[3])
                if variables.has_key('global'): #Checks for global scope
                    globales = variables['global']
                    globales.update(temp_vars)
                    variables['global'] = globales
                else:
                    variables['global'] = temp_vars
            else: #If it is a function
                v_size = 0
                thisElement = { }
                thisElement['type'] = typeID(p[1])
                if p[3].has_key('local_vars'):
                    variables[p[2]] = {}
                    vars_sizeOf[p[2]] = {}
                    if p[3]['local_vars'] is not None:
                        local_vars = p[3]['local_vars'].copy()
                        del p[3]['local_vars']
                        for var_name in local_vars.keys():
                            code = local_vars[var_name]
                            atts = code.split("-")
                            addr = int(atts[0])
                            var_size = int(atts[1])
                            variables[p[2]].update({var_name : addr, 'size' : var_size})
                            vars_sizeOf[p[2]].update({var_name : var_size})
                            v_size += var_size
                    else:
                        local_vars = { }
                        variables[p[2]] = local_vars
                if p[3].has_key('params'):
                    thisElement['param_order'] = p[3]['params']['param_order']
                    del p[3]['params']['param_order']
                    thisElement['params'] = p[3]['params']
                    v_size += len(p[3]['params'])
                else:
                    thisElement['params'] = { }
                thisElement['size'] = v_size
                thisElement['start'] = initQuad_stack.pop()
                procs[p[2]] = thisElement
                scope = p[2]
                if p[3].has_key('vars_identifier'): #Variables called in scope
                    if scope in variables.keys(): #Checks in scope and globally
                        for key in list(p[3]['vars_identifier']):
                            if scopeVarVerif(key, scope):
                                p[3]['vars_identifier'].remove(key)
                    if thisElement.has_key('params'): #Checks in parameters
                        if len(thisElement['params']) > 0:
                            for key in list(p[3]['vars_identifier']): #Checks if functions are type void
                                if key[0] in thisElement['params'].keys() and dataValidation(opTypeConverter(key[1], scope) / 1000, typeVar(p[3]['params'][key[0]]) / 1000, 6, "assignation"):
                                    p[3]['vars_identifier'].remove(key)
                    for key in list(p[3]['vars_identifier']):
                        if key[0] == -1:
                            if opTypeConverter(key[1], scope):
                                p[3]['vars_identifier'].remove(key)
                    if len(p[3]['vars_identifier']) > 0:
                        print "Error: Undeclared variable ", p[3]['vars_identifier'][0][0], " at scope ", scope
                        sys.exit()

#Variable declaration or function declaration
def p_program_aux(p):
    '''program_aux : variable_dec
                   | function_dec'''
    p[0] = p[1]

#Code Statute
def p_code_statute(p):
    '''code_statute : statute code_statute
                      | '''
    if len(p) > 2:
        if p[1] is not None:
            temp_block = p[1]
            if p[2] is not None: #Checks if there was calls to vars or functions, creating or updating the total list
               if temp_block.has_key('call') and p[2].has_key('call'):
                   temp_list = temp_block['call']
                   for call in p[2]['call']:
                       if call not in temp_block['call']:
                           temp_list.append(call)
                   temp_block['call'] = temp_list
                   del p[2]['call']
               else:
                   if p[2].has_key('call'):
                       temp_block['call'] = p[2]['call']
               if temp_block.has_key('temp_vars') and p[2].has_key('temp_vars'):
                   var1_temp = temp_block['temp_vars']
                   var2_temp = p[2]['temp_vars']
                   var1_temp.update(var2_temp)
                   temp_block['temp_vars'] = var1_temp
               else:
                   if p[2].has_key('temp_vars'):
                       temp_block['temp_vars'] = p[2]['temp_vars']
            p[0] = temp_block
        else:
            if p[2] is not None:
                p[0] = p[2]

#Statute
def p_statute(p):
    '''statute : print_statute
                  | ID statute_2
                  | if_statute
                  | while_statute
                  | do_while_statute
                  | type ID variable_dec'''
    if len(p) > 3 and p[1] is not 'return':
        #Variable Declaration
        if p[3] is not None:
            if p[3].has_key('var'):
                if p[3]['var'] == 'var':
                    v_size = 1
                else:
                    v_size = p[3]['var']
                del p[3]['var']
                temp_vars = {p[2] : str(localAddrCalculator(p[1], v_size)) + "-" + str(v_size)}
                for key in p[3].copy():
                    if p[3][key] == 'var':
                        v_size = 1
                    else:
                        v_size = p[3][key]
                    p[3][key] = str(localAddrCalculator(p[1], v_size)) + "-" + str(v_size)
                temp_vars.update(p[3])
                p[0] = {'temp_vars' : temp_vars}
    elif len(p) > 2: #Assignation and call to a function
        if p[2].has_key(103):
            if isinstance(p[2][103], tuple): #If tuple, then there's an array with offset
                offset = p[2][103][0]
                quadGenerator([offset, p[1], 'VER'])
                quad_buffer.append(offset)
                quad_buffer.append("[" + p[1] + "]")
                quadGenerator(['+'])
                tmp = quad_buffer.pop()
                quad_buffer.append("(" + str(tmp) + ")")
                quadGenerator(['='])
            else: #Normal call
                res = p[2][103]
                quad_buffer.append(p[1])
                quadGenerator(["="])
                p[0] = {'call':[(p[1], res)]}
        elif p[2].has_key(105):
            if p[1] not in procs_identifier.keys():
                procs_identifier[p[1]] = p[2][105]
            quadGenerator([p[1], "ERA"]) #ERA quadruple generation
            args = {}
            if p[2].has_key('args'):
                args = p[2]['args']
                params = args[9999]
                param_amount = len(params)
                i = 0
                global param_num
                param_num = param_amount - 1
                while i < param_amount:
                    quadGenerator([p[1]+"-", "param"])
                    i += 1
            else:
                args[9999] = []
            quadGenerator([p[1], "goSub"]) #gotoSub quadruple generation
            p[0] = {'call' : [(-1, {p[1] : args})]} #If -1 then void function, bypassing args return
    elif len(p) > 1 and p[1] is not None:
        p[0] = p[1]

#Statute aux
def p_statute_2(p):
    '''statute_2 : L_PAR const_id_3 R_PAR END_LINE
                   | assign_statute ASSIGN statute_aux'''
    if p[1] != '(':
        if p[1] is not None:
            p[0] = {103 : (p[1]['arr'], p[3])}
        else:
            p[0] = {103 : p[3]} #Assignation
    else:
        if p[2] is not None:
            p[0] = {105 : 4000, 'args' : {9999 : p[2]}}
        else:
            p[0] = {105 : 4000} #Function call used for void

#Statute aux
def p_statute_aux(p):
    '''statute_aux : input_statute
                   | assign_statute_aux END_LINE'''
    p[0] = p[1]

#Function Declaration
def p_function_dec(p):
    '''function_dec : function_id function_call code_statute return_statute BRACES'''
    temp_funct = { }
    if p[1] is not None:
        temp_funct['params'] = p[1]
    if temp_funct is not None and p[3] is not None:
        if p[3].has_key('temp_vars'):
            temp_funct['local_vars'] = p[3]['temp_vars']
        if p[3].has_key('call'):
            temp_funct['vars_identifier'] = p[3]['call']
    p[0] = temp_funct

#FD aux
def p_function_id(p):
    '''function_id : L_PAR function_id_2 R_PAR'''
    p[0] = p[2]

#FD aux
def p_function_id_2(p):
    '''function_id_2 : type params_id function_id_aux function_id_3
                    | '''
    if len(p) > 2:
        temp = {p[2] : localAddrCalculator(p[1], 1)}
        temp.update(p[4])
        if not temp.has_key('param_order'):
            temp['param_order'] = list(params_buffer)
        p[0] = temp

#FD aux
def p_function_id_3(p):
    '''function_id_3 : param_aux function_id_2
                    | '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = { }

#FD aux
def p_function_id_aux(p):
    '''function_id_aux : L_BRACKET exp R_BRACKET
                    | '''

#FD aux
def p_params_id(p):
    '''params_id : ID'''
    params_buffer.append(p[1])
    p[0] = p[1]

#FD aux
def p_param_aux(p):
    '''param_aux : COMMA'''

#FD aux
def p_function_call(p):
    '''function_call : BRACES'''
    initQuad_stack.append(current_quad)

#FD aux
def p_return_statute(p):
    '''return_statute : RETURN return_statute_aux END_LINE'''

#FD aux
def p_return_statute_aux(p):
    '''return_statute_aux : const_var
                        | '''
    global current_quad #Return quad
    if len(p) > 1 and p[1] is not None:
        retn = quad_buffer.pop()
        quadruples.append(["return", retn])
        current_quad += 1
    quadruples.append(["RET"])
    current_quad += 1
    del params_buffer[:]

#Variable Declaration
def p_variable_dec(p):
    '''variable_dec : variable_dec_2 END_LINE'''
    p[0] = p[1]

#VD aux
def p_variable_dec_2(p):
    '''variable_dec_2 : variable_dec_3 variable_dec_aux'''
    var_dict = { 'var' : 'var'}
    if p[1] is not None:
        var_dict['var'] = p[1]
    var_dict.update(p[2])
    p[0] = var_dict

#VD aux
def p_variable_dec_3(p):
    '''variable_dec_3 : L_BRACKET exp R_BRACKET
              | '''
    if len(p) > 1:
        addr_size = quad_buffer.pop()
        if addr_size >= 30000:
            array_size = constants[addr_size]
            p[0] = array_size
        else:
            p[0] = p[2]

#VD aux
def p_variable_dec_aux(p):
    '''variable_dec_aux : COMMA ID variable_dec_2
              | '''
    if len(p) > 3:
        temp_dir = { p[2] : 'var' }
        if p[3] is not None:
            if p[3].has_key('var'):
                temp_dir[p[2]] = p[3]['var']
                del p[3]['var']
                temp_dir.update(p[3])
        p[0] = temp_dir
    else:
        p[0] = { }

#Print
def p_print_statute(p):
    '''print_statute : PRINT L_PAR operation R_PAR END_LINE'''
    quadGenerator(["print"])
    if isinstance(p[3], dict):
        ret = {}
        calls = []
        for key in p[3].keys():
            calls.append( (key, {key : list(p[3][key])}) )
        ret['call'] = calls
        p[0] = ret

#Assignation
def p_assign_statute(p):
    '''assign_statute : L_BRACKET exp R_BRACKET
                     | '''
    if len(p) > 1 and p[1] == '[':
            idxArray = quad_buffer.pop()
            p[0] = {'arr' : idxArray}

#Assign aux
def p_assign_statute_aux(p):
    '''assign_statute_aux : operation'''
    p[0] = p[1]

#Operation
def p_operation(p):
    '''operation : expression operation_aux'''
    if len(p) > 2:
        if p[2] is not None: #If more than one operand, checks compatibility
            if isinstance(p[1], dict): #If dict, it's variable
                var_id = p[1].keys()[0]
                ops = p[1].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    quadGenerator(AndOr_Ops)
                    p[0] = p[1]
                else:
                    ops.append( (3, p[2]) )
                    quadGenerator(AndOr_Ops)
                    p[0] = {var_id : ops}
            elif isinstance(p[2], dict):
                var_id = p[2].keys()[0]
                ops = p[2].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    p[0] = p[2]
                else:
                    ops.append( (3, p[1]) )
                    quadGenerator(AndOr_Ops)
                    p[0] = {var_id : ops}
            else:
                quadGenerator(AndOr_Ops)
                op2 = p[2] / 1000
                action = 3
                op1 = p[1] / 1000
                p[0] = dataValidation(op1, op2, action, "logic")
        else:
            p[0] = p[1]

#Op aux
def p_operation_aux(p):
    '''operation_aux : AO_OPERATOR operation
                    | '''
    if len(p) > 2 and p[2] is not None:
        AndOr_Ops.append(p[1])
        p[0] = p[2]

#Expression
def p_expression(p):
    '''expression : exp expression_aux'''
    if len(p) > 2:
        if p[2] is not None:
            if isinstance(p[1], dict):
                var_id = p[1].keys()[0]
                ops = p[1].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    quadGenerator(logic_Ops)
                    p[0] = p[1]
                else:
                    if '>' in p[2].keys():
                        ops.append( (4, p[2]['>']) )
                    elif '>=' in p[2].keys():
                        ops.append( (4, p[2]['>=']) )
                    elif '<' in p[2].keys():
                        ops.append( (4, p[2]['<']) )
                    elif '<=' in p[2].keys():
                        ops.append( (4, p[2]['<=']) )
                    elif '==' in p[2].keys():
                        ops.append( (5, p[2]['==']) )
                    quadGenerator(logic_Ops)
                    p[0] = {var_id : ops}
            else:
                quadGenerator(logic_Ops)
                if '>' in p[2].keys():
                    action = 4
                    op2 = p[2]['>'] / 1000
                elif '>=' in p[2].keys():
                    action = 4
                    op2 = p[2]['>='] / 1000
                elif '<' in p[2].keys():
                    action = 4
                    op2 = p[2]['<'] / 1000
                elif '<=' in p[2].keys():
                    action = 4
                    op2 = p[2]['<='] / 1000
                elif '==' in p[2].keys():
                    action = 5
                    op2 = p[2]['=='] / 1000
                op1 = p[1] / 1000
                p[0] = dataValidation(op1, op2, action, "Value comparison")
        else:
            p[0] = p[1]

#Expression aux
def p_expression_aux(p):
    '''expression_aux : LOGIC_OPERATOR exp
                    | '''
    if len(p) > 2 and p[2] is not None:
        logic_Ops.append(p[1])
        p[0] = {p[1] : p[2]}

#Factor
def p_factor(p):
    '''factor : L_PAR expression R_PAR
                | const_var
                | AS_OPERATOR const_var'''
    if len(p) > 3:
        p[0] = p[2]
    elif len(p) > 2:
        if 0 in constants.values(): #0 stored as const
            zero_addr = constants.keys()[constants.values().index(0)]
        else:
            zero_addr = constAddrCalculator("int")
            constants[zero_addr] = 0
        global quad_buffer #Quadruples generation
        quad_buffer.insert(len(quad_buffer) - 1, zero_addr)
        quadGenerator(["-"])
        p[0] = p[2]
    elif len(p) > 1:
        p[0] = p[1]

#Exp
def p_exp(p):
    '''exp : term exp_aux'''
    if len(p) > 2:
        if p[2] is not None:
            if isinstance(p[1], dict):
                var_id = p[1].keys()[0]
                ops = p[1].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    quadGenerator(AddSub_Ops)
                    p[0] = p[1]
                else:
                    ops.append( (1, p[2]) )
                    quadGenerator(AddSub_Ops)
                    p[0] = {var_id : ops}
            elif isinstance(p[2], dict):
                var_id = p[2].keys()[0]
                ops = p[2].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    p[0] = p[2]
                else:
                    ops.append( (1, p[1]) )
                    quadGenerator(AddSub_Ops)
                    p[0] = {var_id : ops}
            else:
                quadGenerator(AddSub_Ops)
                op2 = p[2] / 1000
                action = 1
                op1 = p[1] / 1000
                p[0] = dataValidation(op1, op2, action, "Additon / Substraction")
        else:
            p[0] = p[1]

#Exp aux
def p_exp_aux(p):
    '''exp_aux : AS_OPERATOR exp
              | '''
    if len(p) > 2 and p[2] is not None:
        AddSub_Ops.append(p[1])
        p[0] = p[2]

#Term
def p_term(p):
    '''term : factor term_aux'''
    if len(p) > 2:
        if p[2] is not None:
            if isinstance(p[1], dict):
                var_id = p[1].keys()[0]
                ops = p[1].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    quadGenerator(MultDiv_Ops)
                    p[0] = p[1]
                else:
                    ops.append( (2, p[2]) )
                    quadGenerator(MultDiv_Ops)
                    p[0] = {var_id : ops}
            elif isinstance(p[2], dict):
                var_id = p[2].keys()[0]
                ops = p[2].values()[0]
                if isinstance(ops, dict) and ops.has_key(9999):
                    p[0] = p[2]
                else:
                    ops.append( (2, p[1]) )
                    quadGenerator(MultDiv_Ops)
                    p[0] = {var_id : ops}
            else:
                quadGenerator(MultDiv_Ops)
                op2 = p[2] / 1000
                action = 2
                op1 = p[1] / 1000
                p[0] = dataValidation(op1, op2, action, "Multiplication / Division")
        else:
            p[0] = p[1]

#Term aux
def p_term_aux(p):
    '''term_aux : MD_OPERATOR term
                  | '''
    if len(p) > 2 and p[2] is not None:
        MultDiv_Ops.append(p[1])
        p[0] = p[2]

#While
def p_while_statute(p):
    '''while_statute : WHILE L_PAR operation while_init BRACES code_statute while_end'''
    ret = p[6]
    if ret is not None:
        if isinstance(p[3], dict):
            if ret.has_key('call'):
                calls = ret['call']
                for key in p[3].keys():
                    calls.append( (key, {key : list(p[3][key])}) )
                ret['call'] = calls
            else:
                calls = []
                for key in p[3].keys():
                    calls.append( (key, {key : list(p[3][key])}) )
                ret['call'] = calls
        p[0] = ret

#While Init
def p_while_init(p):
    '''while_init : R_PAR'''
    goto_stack.append(current_quad)
    quadGenerator(["gotoF"])

#While End
def p_while_end(p):
    '''while_end : BRACES'''
    last_goto = goto_stack.pop()
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = current_quad + 1
        quadruples[last_goto] = goto_quad
    quadGenerator(["goto"]) #Quad to return to comparison
    last_goto = goto_stack.pop() #Fills last goto
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = goto_stack.pop() - 1 #If -1 returns to comparison
        quadruples[last_goto] = goto_quad

#While
def p_do_while_statute(p):
    '''do_while_statute : DO do_while_init code_statute BRACES WHILE L_PAR operation do_while_end'''
    ret = p[3]
    if ret is not None:
        if isinstance(p[7], dict):
            if ret.has_key('call'):
                calls = ret['call']
                for key in p[7].keys():
                    calls.append( (key, {key : list(p[7][key])}) )
                ret['call'] = calls
            else:
                calls = []
                for key in p[7].keys():
                    calls.append( (key, {key : list(p[7][key])}) )
                ret['call'] = calls
        p[0] = ret

#While Init
def p_do_while_init(p):
    '''do_while_init : BRACES'''
    goto_stack.append(current_quad)
    quadGenerator(["gotoF"])

#While End
def p_do_while_end(p):
    '''do_while_end : R_PAR'''
    last_goto = goto_stack.pop()
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = current_quad + 1
        quadruples[last_goto] = goto_quad
    quadGenerator(["goto"]) #Quad to return to comparison
    last_goto = goto_stack.pop() #Fills last goto
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = goto_stack.pop() - 1 #If -1 returns to comparison
        quadruples[last_goto] = goto_quad

#If
def p_if_statute(p):
    '''if_statute : IF L_PAR operation if_init BRACES code_statute BRACES if_statute_aux'''
    last_goto = goto_stack.pop()
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = current_quad
        quadruples[last_goto] = goto_quad
    ret = p[6]
    if ret is not None:
        if isinstance(p[3], dict):
            if ret.has_key('call'):
                calls = ret['call']
                for key in p[3].keys():
                    calls.append( (key, {key : list(p[3][key])}) )
                ret['call'] = calls
            else:
                calls = []
                for key in p[3].keys():
                    calls.append( (key, {key : list(p[3][key])}) )
                ret['call'] = calls
        p[0] = ret

#If aux
def p_if_statute_aux(p):
    '''if_statute_aux : else_statute BRACES code_statute BRACES
             | '''

#Else
def p_else_statute(p):
    '''else_statute : ELSE'''
    last_goto = goto_stack.pop() #Modifies if quad with else
    goto_quad = quadruples[last_goto]
    if goto_quad[-1] == -1:
        goto_quad[-1] = current_quad + 1
        quadruples[last_goto] = goto_quad
    quadGenerator(["goto"])

#Input
def p_input_statute(p):
    '''input_statute : INPUT L_PAR type R_PAR END_LINE'''
    quad_buffer.append(p[3])
    quadGenerator(["input"])
    p[0] = typeID(p[3])

#Constant
def p_const_var(p):
    '''const_var : const_int
                   | const_float
                   | const_boolean
                   | const_id'''
    if len(p) > 1 and p[1] is not None:
        p[0] = p[1]

#Int Constant
def p_const_int(p):
    '''const_int : INT'''
    if p[1] in constants.values(): #Checks if constant already exists
        const_addr = constants.keys()[constants.values().index(p[1])]
    else:
        const_addr = constAddrCalculator("int")
        constants[const_addr] = p[1]
    quad_buffer.append(const_addr)
    p[0] = 1000

#Float Constant
def p_const_float(p):
    '''const_float : FLOAT'''
    if p[1] in constants.values():
        const_addr = constants.keys()[constants.values().index(p[1])]
    else:
        const_addr = constAddrCalculator("float")
        constants[const_addr] = p[1]
    quad_buffer.append(const_addr)
    p[0] = 2000

#Bool Constant
def p_const_boolean(p):
    '''const_boolean : BOOLEAN'''
    if p[1] in constants.values():
        const_addr = constants.keys()[constants.values().index(p[1])]
    else:
        const_addr = constAddrCalculator("boolean")
        constants[const_addr] = p[1]
    quad_buffer.append(const_addr)
    p[0] = 3000

#Constant ID
def p_const_id(p):
    '''const_id : ID const_id_2'''
    if len(p) > 2: #Checks type and if it is declared, return
        quad_buffer.append(p[1])
        if p[2] is not None:
            if p[2].has_key('func'):
                cid_data = p[2]['func']
                quadGenerator([p[1], "ERA"])
                param_amount = len(cid_data) #Parameters
                i = 0
                func_name = quad_buffer.pop()
                global param_num
                param_num = param_amount - 1
                while i < param_amount: #Generates a quadruple for each param
                    quadGenerator([p[1]+"-", "param"])
                    i += 1
                quadGenerator([p[1], "goSub"]) #Generates goto function quadruple
                quad_buffer.append(func_name)
                p[0] = { p[1] : {9999  : cid_data} }
            elif p[2].has_key('arr'):
                quad_buffer.pop()
                offset = p[2]['arr']
                quadGenerator([offset, p[1], 'VER'])
                quad_buffer.append(offset)
                quad_buffer.append("[" + p[1] + "]")
                quadGenerator(['+'])
                res = quad_buffer.pop()
                quad_buffer.append("(" + res + ")")
                p[0] = {p[1] : []}
        else:
            p[0] = {p[1] : []}

#Constant ID aux
def p_const_id_2(p):
    '''const_id_2 : L_BRACKET exp R_BRACKET
                    | L_PAR const_id_3 R_PAR
                    | '''
    if len(p) > 2:
        if p[1] == '(':
            p[0] = { 'func':p[2] }
        elif p[1] == '[':
            p[0] = {'arr' : quad_buffer.pop()}

#Constant ID aux
def p_const_id_3(p):
    '''const_id_3 : const_var const_id_aux
                    | '''
    if len(p) > 2:
        args = [p[1]]
        if p[2] is not None:
            args = args + p[2]
        p[0] = args

#Constant ID aux
def p_const_id_aux(p):
    '''const_id_aux : COMMA const_id_3
                    | '''
    if len(p) > 2:
        p[0] = p[2]

#Type
def p_type(p):
    '''type : TYPE_INT
            | TYPE_FLOAT
            | TYPE_BOOLEAN
            | TYPE_VOID'''
    p[0] = p[1]

#If Init
def p_if_init(p):
    '''if_init : R_PAR'''
    quadGenerator(["gotoF"])

#Parsing error function
def p_error(p):
    print "Parsing Error: ", p
    sys.exit()

lex.lex()
yacc.yacc()

#Input file management
filename = raw_input("Filename: ")
fileX = open(filename, 'r')
data = fileX.read()
yacc.parse(data)

#Generates the virtual machine and calls it for execution
virtual_machine = VirtualMachine(constants, quadruples)
virtual_machine.runProgram()
