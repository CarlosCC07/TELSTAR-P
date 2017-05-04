##############################
#                            #
#   Telstar+ Aux Functions   #
#                            #
##############################

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
