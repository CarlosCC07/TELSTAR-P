##############################
#                            #
# Cubo semantico de Telstar+ #
#                            #
##############################

from collections import defaultdict
semantic_cube = defaultdict(lambda :defaultdict(lambda :defaultdict(int)))

#Index
#
# x = operador 1
# y = operador 2
# z = operando
#

#Formato
#
# semantic_cube[x][y][z]
#

#Datos
#
# Int: 1
# Float: 2
# Boolean: 3
#

#Identificadores de los operadores
#
# +, -: 1
# *, /: 2
# &&, ||: 3
# <, <=, >, >=: 4
# ==, !=: 5
# =: 6

#Error = -1

#Suma y Resta (+ y -)
dataMatches[1][1][1] = 1
dataMatches[1][2][1] = 2
dataMatches[1][3][1] = -1
dataMatches[2][1][1] = 2
dataMatches[2][2][1] = 2
dataMatches[2][3][1] = -1
dataMatches[3][1][1] = -1
dataMatches[3][2][1] = -1
dataMatches[3][3][1] = -1


#Mult y Div (* y /)
dataMatches[1][1][2] = 1
dataMatches[1][2][2] = 2
dataMatches[1][3][2] = -1
dataMatches[2][1][2] = 2
dataMatches[2][2][2] = 2
dataMatches[2][3][2] = -1
dataMatches[3][1][2] = -1
dataMatches[3][2][2] = -1
dataMatches[3][3][2] = -1


#AND/OR (&& y ||)
dataMatches[1][1][3] = 1
dataMatches[1][2][3] = -1
dataMatches[1][3][3] = -1
dataMatches[2][1][3] = -1
dataMatches[2][2][3] = 1
dataMatches[2][3][3] = -1
dataMatches[3][1][3] = -1
dataMatches[3][2][3] = -1
dataMatches[3][3][3] = 1

#Comparadores (<, <=, > y >=)
dataMatches[1][1][4] = 1
dataMatches[1][2][4] = 1
dataMatches[1][3][4] = -1
dataMatches[2][1][4] = 1
dataMatches[2][2][4] = 1
dataMatches[2][3][4] = -1
dataMatches[3][1][4] = -1
dataMatches[3][2][4] = -1
dataMatches[3][3][4] = -1

#Igualdad (== y !=)
dataMatches[1][1][5] = 1
dataMatches[1][2][5] = 1
dataMatches[1][3][5] = -1
dataMatches[2][1][5] = 1
dataMatches[2][2][5] = 1
dataMatches[2][3][5] = -1
dataMatches[3][1][5] = -1
dataMatches[3][2][5] = -1
dataMatches[3][3][5] = 3

#Asignacion (=)
dataMatches[1][1][6] = 1
dataMatches[1][2][6] = 1
dataMatches[1][3][6] = -1
dataMatches[2][1][6] = 1
dataMatches[2][2][6] = 1
dataMatches[2][3][6] = -1
dataMatches[3][1][6] = -1
dataMatches[3][2][6] = -1
dataMatches[3][3][6] = 1

#Funcion para realizar la consulta al cubo y defenir el tipo del resultado
def matchOp(op1, op2, operator):
	return matchData[op1][op2][operator]
