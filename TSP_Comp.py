#Compilador Telstar+

import ply.lex as lex
import ply.yacc as yacc
#import cubo semantico
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
    errors = True
    return t

#---------------------------------------------------------------------#
#                    REGLAS GRAMATICALES - TELSTAR+                   #
#---------------------------------------------------------------------#

#Direcciones de Memoria

#Tablas de constantes
procedures = { }
variables = { }
scope = 'global'

#PROGRAM
def p_program(p):
    '''program : PROGRAM ID END_LINE global_variable_dec function_dec L_BRACE code_statute R_BRACE'''
    mainVars = { }
    mainVars['main'] = p[4]
    variables.update(mainVars)
    print("Succesful Program Build")

    ##Todo lo que sigue son debugs
    #print ("\n")
    #print ("Debug Messages:")
    #print ("Procedures:")
    #print (procedures) #Debug para la tabla de funciones, eliminar
    #print ("\n")
    #print ("Variables:")
    #print (variables)
    #print ("\n")

#Empty
def p_empty(p):
    '''empty : '''
    pass


#Declaración de Variables (globales u otras)
def p_global_variable_dec(p):
    '''global_variable_dec : vd_2 END_LINE
                      | empty'''

def p_vd_2(p):
    '''vd_2 : type ID variable_dec_multi'''

def p_variable_dec_multi(p):
    '''variable_dec_multi : COMMA vd_2
                            | empty'''

def p_local_var_dec(p):
    '''local_var_dec : type ID local_multivar_dec END_LINE'''

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
    #p[0] = p[1]

def p_function_call(p):
    '''function_call : CALL ID LEFT_PAR exp cm_2 RIGHT_PAR END_LINE'''

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

#Asignacion
def p_assign_statute(p):
    '''assign_statute : ID array_assign_statute ASSIGN logical_exp END_LINE'''

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
