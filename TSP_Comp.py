#Compilador Telstar+

import ply.lex as lex
import ply.yacc as yacc
from sys import *
from semantic_cube import matchData
#from argparse import _ActionsContainer

#import maquina virtual

#---------------------------------------------------------------------#
#                          LEXICO - TELSTAR+                          #
#---------------------------------------------------------------------#

#Tokens
reserved = {
   'program' : 'PROGRAM',
   #'begin' : 'BEGIN',
   #'end' : 'END',
   'int' : 'TYPE_INT',
   'float' : 'TYPE_FLOAT',
   'boolean' : 'TYPE_BOOLEAN',
   'define' : 'DEFINE',
   'call' : 'CALL',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'do' : 'DO',
   'return' : 'RETURN',
   'print' : 'PRINT',
   'dot' : 'DOT',
   'line' : 'LINE',
   'curve' : 'CURVE'
   'main' : 'MAIN',
}

tokens = ['INT', 'BOOLEAN', 'FLOAT', 'END_LINE', 'COMMA', 'L_BRACE', 'R_BRACE', 'LEFT_PAR', 'RIGHT_PAR', 'L_BRACKET', 'R_BRACKET', 'LOGIC_OPERATOR', 'COND_OPERATOR', 'AS_OPERATOR', 'MD_OPERATOR', 'ASSIGN', 'ID'] + list(reserved.values())

t_ignore = ' \t\n'

#IDs
def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9]*'
    token.type = reserved.get(token.value,'ID')
    return token

#Types
def t_INT(token):
    r'[0-9]+'
    token.value = int(token.value);
    return token

def t_FLOAT(token):
    r'[0-9]*\.[0-9]+'
    token.value = float(token.value)
    return token

def t_BOOLEAN(token):
    r'true|false'
    return token

#Operators
def t_LOGIC_OPERATOR(token):
    r'&&|\|\|'
    return token

def t_COND_OPERATOR(token):
    r'>|<|>=|<=|==|!='
    return token

def t_AS_OPERATOR(token):
    r'\+|\-'
    return token

def t_MD_OPERATOR(token):
    r'\*|/'
    return token

def t_ASSIGN(token):
    r'='
    return token

#Symbols
def t_END_LINE(token):
    r'\;'
    return token

def t_COMMA(token):
    r'\,'
    return token

def t_L_BRACE(token):
    r'\{'
    return token

def t_R_BRACE(token):
    r'\}'
    return token

def t_L_BRACKET(token):
    r'\['
    return token

def t_R_BRACKET(token):
    r'\]'
    return token

def t_LEFT_PAR(token):
    r'\('
    return token

def t_RIGHT_PAR(token):
    r'\)'
    return token

#Errores de sintaxis
def t_error(t):
    print('Syntax Error: Invalid character ' + str(t.value[0]))
    sys.exit()
    return t

#---------------------------------------------------------------------#
#                    REGLAS GRAMATICALES - TELSTAR+                   #
#---------------------------------------------------------------------#

#Direcciones virtuales
dv_int = 0
dv_float = 1000
dv_bool = 2000

#Tablas de variables y procedimientos, identificadores (en el sufijo) y manejo para las no declaradas (prefijo ud)
procs = { }
variables = { }
vars_identifier = []
procs_identifier = {}
ud_vars = []
ud_procs = []

#Variables para generacion y manejo de cuadruplos
quadr_buffer = []
quadruples = []
temp_cont = 1
md_buffer = []
sr_buffer = []
logic_buffer = []
cond_buffer = []
current_quadr = 0
conditions = []
jumps = []

#Scope
scope = ''

#Verifica si la variable ya existe en el scope, ya sea local o global
def scopeVarVerif(var, scope):
    if var[0] in variables[scope]:
        type1 = typeVar(variables[scope][var[0]])
        type2 = opTypeConverter(var[1], scope)

        if dataValidation(type1 / 1000, type2 / 1000, 6, "assign"):
            return True

    elif 'global' in variables.keys():
        if var[0] in variables['global']:
            type1 = typeVar(variables['global'][var[0]])
            type2 = opTypeConverter(var[1], 'global')

            if dataValidation(type1 / 1000, type2 / 1000, 6, "assign"):
                return True
        else:
            return False

#Verifica que los tipos de datos en las operaciones sean validos
def dataValidation(op1, op2, operator, message):
    if semantic_cube.matchData(op1, op2, operator) == -1:
        print("Error: Non-compatible data types in operation " + message)
        sys.exit()
    else:
        return matchData.getResultType(op1, op2, operator) * 1000

#Calcula la direccion base correspondiente dependiendo del tipo de asignacion
def addressCalculator(typeX):
    if typeX == 'int':
        global dv_int
        dv_int += 1
        return dv_int - 1
    elif typeX == 'float':
        global dv_float
        dv_float += 1
        return dv_float - 1
    else:
        global dv_bool
        dv_bool += 1
        return dv_bool - 1

#Calcula el identificador numerico del tipo dependiendo de la direccion base
def typeVar(address):
    if address < 1000:
        return 1000
    elif address >= 1000 and address < 2000:
        return 2000
    else:
        return 3000

#Regresa el tipo dependiendo del identificador numerico
def typeName(typeIDX):
    if typeIDX == 1000:
        return 'int'
    elif typeIDX == 2000:
        return 'float'
    elif typeIDX == 3000:
        return 'boolean'
    else:
        return 'void'

#Regresa el identificador numerico dependiendo del tipo
def typeID(typeX):
    if typeX == 'int':
        return 1000
    elif typeX == 'float':
        return 2000
    elif typeX == 'boolean':
        return 3000
    elif tipo == 'void':
        return 4000

#Interpretar los dicts que contienen los ordenes de operaciones
def opTypeConverter(dic, scope):
    #Ejecuta opcion 1 si ya es un tipo, 2 si es una lista de ops, o 3 si hay variable
    if isinstance(dic, int):
        return dic
    elif isinstance(dic, list):
        print(dic)
    elif isinstance(dic, dict):
        var1 = d.keys()[0]

        if var1 in variables[scope].keys():
            type1 = typeVar(variables[scope][var1])
            return opTypeAux(dic[var1], type1, scope)
        elif var1 in procs.keys() and dic[var1].has_key(9999): #El 9999 indica que es funcion
            #Verificacion de argumentos en los llamados
            if dic[var1][9999] is not None:
                argsCalled = dic[var1][9999]
                funcArgs = list(procs[var1]['params'].values())

                if len(argsCalled) != len(functArgs):
                    print("Error: argument number in function " + str(var1))
                    sys.exit()

                for arg in argsCalled:
                    for param in procs[var1]['params'].values():
                        if dataValidation(arg / 1000, typeVar(param) / 1000, 6, "assign"):
                            functArgs.remove(param)

                if len(functArgs) == 0:
                    return procs[var1]['type']
                else:
                    print("Error: wrong argument type in function" +  str(var1))
                    sys.exit()
            else:
                #Si no se esperan argumentos
                if len(procs[var1]['params'].keys()) == 0:
                    return procs[var1]['type']
                else:
                    print("Error: expected arguments in function " +  str(var1))
                    sys.exit()
        #Si no esta previamente declarada
        else:
            print("Error: undeclared variable or function" + str(var1))
            sys.exit()

#Auxuliar para checar las listas con operaciones
def opTypeAux(op_list, type1, scope):

    for op in op_list:
        oper = op[0]

        if isinstance(op[1], dict):
            type2 = opTypeConverter(op[1], scope)
        else:
            type2 = op[1]

        type1 = isCompatible(type1 / 1000, type2 / 1000, oper, "assign")

    return type1

#Generacion de cuadruplos usando tuplas
def quadGenerator(sign):
    global quadr_buffer
    global temp_cont
    global current_quadr

    if len(quadr_buffer) > 0:
        op1 = quadr_buffer.pop()
        temp = "T" + str(temp_cont)
        opr = sign.pop()
        #Asignaciones
        if opr == "=":
            if len(quadr_buffer) > 0:
                op2 = quadr_buffer.pop()
                quad = [opr, op2, op1]
        #Impresion
        elif opr == "print":
            quad = [opr, op1]
        #Dibujo
        elif opr == "line":
            quad = [opr, op1]
        elif opr == "dot":
            quad = [opr, op1]
        elif opr == "curve":
            quad = [opr, op1]
        #Go to False
        elif opr == "gotoF":
            place = conditions.pop()
            quad = [opr, op1, "..."]
            quadruples.insert(place, quad)
            jumps.append(place)
            print ("Debug -> jumps" + str(jumps))
            current_quadr += 1
            return
        #Operaciones Matematicas
        else:
            if len(quadr_buffer) > 0:
                op2 = quadr_buffer.pop()
                quad = [opr, op2, op1, temp]
                quadr_buffer.append(temp)
                temp_cont += 1
        quadruples.append(quad)
        current_quadr += 1

#Maneja los cuadruplos pendientes
def quadFinish():
    if len(jumpd) > 0:
        iP = jumps.pop()
        pend = quadruples[14]
        print("Pending: " + str(pend))


#PROGRAM
def p_program(p):
    '''program : PROGRAM ID END_LINE global_variable_dec function_dec MAIN L_BRACE code_statute R_BRACE'''
     #Variables Declaradas
    mainVars = { }
    mainVars['main'] = p[4]
    variables.update(mainVars)

    #Resto de las variables
    for key in calledVars:
        if key in variables['main'] or key in variables['global']:
            calledVars.remove(key)
        else:
            print "Error: Undeclared variable " + key
            sys.exit()

    for key in calledProcs:
        if key in procedures.keys():
            calledProcs.remove(key)
        else:
            print "Error! Undeclared function: " + key
            sys.exit()

    print("Succesful Program Build")

    #Todo lo que sigue son debugs
    print "-----------\nDebug Messages!\n"
    print "Procedures:"
    print procedures #Debug para la tabla de funciones, eliminar
    print "\nVariables:"
    print variables
    print "\n"

#Empty
def p_empty(p):
    '''empty : '''
    pass


#Declaración de Variables (globales u otras)
def p_global_variable_dec(p):
    '''global_variable_dec : vd_2 END_LINE
                      | empty'''
    p[0] = p[1]

def p_vd_2(p):
    '''vd_2 : type ID variable_dec_multi'''
    for key in p[3]:
        p[3][key] = p[1]

    tempVars = {p[2] : p[1]}
    tempVars.update(p[3])

    #Se checa si hay un scope global
    if variables.has_key('global'):
        globales = variables['global']
        globales.update(tempVars)
        variables['global'] = globales
    else:
        variables['global'] = tempVars

def p_variable_dec_multi(p):
    '''variable_dec_multi : COMMA vd_2
                            | empty'''

def p_local_var_dec(p):
    '''local_var_dec : type ID local_multivar_dec END_LINE'''
    thisElement = { }
    thisElement['type'] = p[1]
    if p[3].has_key('localVars'):
        if p[3]['localVars'] is not None:
            localVars = p[3]['localVars'].copy()
            del p[3]['localVars']
            variables[p[2]] = localVars

    thisElement['params'] = p[3]
    procedures[p[2]] = thisElement
    scope = p[2]

    #Checar si las asignaciones existen en el scope o son argumentos actuales
    for key in calledVars:
        if key in p[3].keys():
            calledVars.remove(key)
    #Ambas comparaciones dentro de un mismo for no jalan... se soluciona usando dos fors! :D
    for key in calledVars:
        if key in variables[scope].keys():
            calledVars.remove(key)

    #Checar si es el nombre de alguna funcion, y de serlo, comparar argumentos (pendiente)
    for key in calledProcs:
        if key in procedures.keys():
            calledProcs.remove(key)
            #Agregar aqui lo de los parametros
    p[0] = p[1]

def p_local_multivar_dec(p):
    '''local_multivar_dec : COMMA local_var_dec
                            | empty'''


#Estatuto de codigo
def p_code_statute(p):
    '''code_statute : statute code_statute
                      | empty'''
    if len(p) > 2:
        if p[1] is not None:
            tempBloque = p[1]
            if p[2] is not None:
                tempBloque.update(p[2])

            p[0] = tempBloque
        else:
            if p[2] is not None:
                p[0] = p[2]


#def p_code_statute_multi(p):
#    '''code_statute_multi : cs_2'''

#Tipo de entrada
def p_type(p):
    '''type : TYPE_INT array_dec
              | TYPE_FLOAT array_dec
              | TYPE_BOOLEAN array_dec'''

#Data
def p_data(p):
    '''data : INT
              | FLOAT
              | BOOLEAN'''


#Array
def p_array_dec(p):
    '''array_dec : L_BRACKET INT R_BRACKET
                   | empty'''


#Funcion
def p_function_dec(p):
    '''function_dec : DEFINE type ID LEFT_PAR params RIGHT_PAR L_BRACE code_statute R_BRACE
                      | empty'''
    tempFunc = { }
    if p[1] is not None:
        tempFunc.update(p[1])
    if tempFunc is not None:
        tempFunc['localVars'] = p[3]
    p[0] = tempFunc
    p[0] = p[2]

def p_function_call(p):
    '''function_call : CALL ID LEFT_PAR exp cm_2 RIGHT_PAR END_LINE'''
    p[0] = 105 #Codigo de llamada a funcion
    if p[2] == 105:
        calledProcs.append(p[1])

def p_cm_2(p):
    '''cm_2 : COMMA call_multi
              | empty'''

def p_call_multi(p):
    '''call_multi : exp cm_2
                    | empty'''

def p_params(p):
    '''params : type ID  param_array params_multi
                | empty'''
    if len(p) > 2:
        temp = {p[2] : p[1]}
        temp.update(p[4])
        p[0] = temp

def p_param_array(p):
    '''param_array : L_BRACKET exp R_BRACKET
                     | empty'''

def p_params_multi(p):
    '''params_multi : COMMA params
                      | empty'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = { }


#Estatuto
def p_statute(p):
    '''statute : assign_statute
                 | if_statute
                 | while_statute
                 | do_while_statute
                 | return_statute
                 | print_statute
                 | draw_statute
                 | local_var_dec
                 | function_call'''
    if len(p) > 3:
        #Declaraciones de variables
        if p[3] is not None:
            for key in p[3]:
                p[3][key] = p[1]

            tempVars = {p[2] : p[1]}
            tempVars.update(p[3])
            p[0] = tempVars
    #Asignacion y llamada a funcion
    elif len(p) > 2:
        if p[2] == 103:
            calledVars.append(p[1])
        elif p[2] == 105:
            calledProcs.append(p[1])

#Asignacion
def p_assign_statute(p):
    '''assign_statute : ID array_assign_statute ASSIGN logical_exp END_LINE'''
    p[0] = 103 #Codigo de asignacion
    if p[2] == 103:
        calledVars.append(p[1])


def p_array_assign_statute(p):
    '''array_assign_statute : L_BRACKET exp R_BRACKET
                              | empty'''


#If
def p_if_statute(p):
    '''if_statute : IF LEFT_PAR logical_exp RIGHT_PAR L_BRACE code_statute R_BRACE if_else END_LINE'''

def p_if_else(p):
    '''if_else : ELSE L_BRACE code_statute R_BRACE
                 | empty'''


#While
def p_while_statute(p):
    '''while_statute : WHILE LEFT_PAR logical_exp RIGHT_PAR L_BRACE code_statute R_BRACE END_LINE'''


#Do While
def p_do_while_statute(p):
    '''do_while_statute : DO L_BRACE code_statute R_BRACE WHILE LEFT_PAR logical_exp RIGHT_PAR END_LINE'''


#Return Statute
def p_return_statute(p):
    '''return_statute : RETURN logical_exp END_LINE'''


#Print Statute
def p_print_statute(p):
    '''print_statute : PRINT LEFT_PAR logical_exp multi_print_statute RIGHT_PAR END_LINE'''

def p_multi_print_statute(p):
    '''multi_print_statute : COMMA logical_exp print_2
                             | empty'''

def p_print_2(p):
    '''print_2 : multi_print_statute'''


#Draw Statute
def p_draw_statute(p):
    '''draw_statute : draw_point
                      | draw_line
                      | draw_curve'''


#Draw Point
def p_draw_point(p):
    '''draw_point : DOT LEFT_PAR logical_exp COMMA logical_exp point_extra_1 RIGHT_PAR END_LINE'''

def p_point_extra_1(p):
    '''point_extra_1 : COMMA logical_exp point_extra_2
                       | empty'''

def p_point_extra_2(p):
    '''point_extra_2 : COMMA logical_exp
                       | empty'''


#Draw Line
def p_draw_line(p):
    '''draw_line : LINE LEFT_PAR logical_exp COMMA logical_exp COMMA logical_exp line_extra_1 RIGHT_PAR END_LINE'''

def p_line_extra_1(p):
    '''line_extra_1 : COMMA logical_exp line_extra_2
                      | empty'''

def p_line_extra_2(p):
    '''line_extra_2 : COMMA logical_exp
                      | empty'''


#Draw Curve
def p_draw_curve(p):
    '''draw_curve : CURVE LEFT_PAR logical_exp COMMA logical_exp COMMA logical_exp COMMA logical_exp curve_extra_1 RIGHT_PAR END_LINE'''

def p_curve_extra_1(p):
    '''curve_extra_1 : COMMA logical_exp curve_extra_2
                       | empty'''

def p_curve_extra_2(p):
    '''curve_extra_2 : COMMA logical_exp
                       | empty'''

#Logical Exp
def p_logical_exp(p):
    '''logical_exp : cond_exp logical_exp_2'''

def p_logical_exp_2(p):
    '''logical_exp_2 : LOGIC_OPERATOR cond_exp
                       | empty'''


#Cond Exp
def p_cond_exp(p):
    '''cond_exp : exp cond_exp_2'''

def p_cond_exp_2(p):
    '''cond_exp_2 : COND_OPERATOR exp
                    | empty'''


#Exp
def p_exp(p):
    '''exp : term exp_2'''

def p_exp_2(p):
    '''exp_2 : AS_OPERATOR term
               | empty'''


#Termino
def p_term(p):
    '''term : factor term_2'''

def p_term_2(p):
    '''term_2 : MD_OPERATOR factor
                | empty'''


#Factor
def p_factor(p):
    '''factor : LEFT_PAR logical_exp RIGHT_PAR
                | factor_2 const_var'''

def p_factor_2(p):
    '''factor_2 : AS_OPERATOR
                  | empty'''


#Constante
def p_const_var(p):
    '''const_var : data
                   | id_oper'''


#ID Oper
def p_id_oper(p):
    '''id_oper : ID id_oper_2'''

def p_id_oper_2(p):
    '''id_oper_2 : L_BRACKET exp R_BRACKET
                   | LEFT_PAR id_oper_3 RIGHT_PAR
                   | empty'''

def p_id_oper_3(p):
    '''id_oper_3 : exp id_oper_multi
                   | empty'''

def p_id_oper_multi(p):
    '''id_oper_multi : COMMA exp id_multi_2
                   | empty'''

def p_id_multi_2(p):
    '''id_multi_2 : id_oper_multi'''

#Funcion de error para el parser
def p_error(p):
    print("Parsing error at: ")
    print(p)
    return(p)

#Inicializacion del Lex
lex.lex()

#Inicializacion del Parser
yacc.yacc()

fileName = input("Filename: ")

fileX = open(fileName, 'r')

data = fileX.read()

yacc.parse(data)
