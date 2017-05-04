##############################
#                            #
#   Telstar+ Semantic Cube   #
#                            #
##############################

from collections import defaultdict
semantic_cube = defaultdict(lambda :defaultdict(lambda :defaultdict(int)))

#Int: 1
#Float: 2
#Boolean: 3
#Error: -1

#Addition and Substraction operators (+ -)
semantic_cube[1][1][1] = 1
semantic_cube[1][2][1] = 2
semantic_cube[1][3][1] = -1
semantic_cube[2][1][1] = 2
semantic_cube[2][2][1] = 2
semantic_cube[2][3][1] = -1
semantic_cube[3][1][1] = -1
semantic_cube[3][2][1] = -1
semantic_cube[3][3][1] = -1

#Multiplication and Division operators (* /)
semantic_cube[1][1][2] = 1
semantic_cube[1][2][2] = 2
semantic_cube[1][3][2] = -1
semantic_cube[2][1][2] = 2
semantic_cube[2][2][2] = 2
semantic_cube[2][3][2] = -1
semantic_cube[3][1][2] = -1
semantic_cube[3][2][2] = -1
semantic_cube[3][3][2] = -1

#AND OR Operators (&& ||)
semantic_cube[1][1][3] = 1
semantic_cube[1][2][3] = -1
semantic_cube[1][3][3] = -1
semantic_cube[2][1][3] = -1
semantic_cube[2][2][3] = 1
semantic_cube[2][3][3] = -1
semantic_cube[3][1][3] = -1
semantic_cube[3][2][3] = -1
semantic_cube[3][3][3] = 1


#Logic Operators (< <= > >=)
semantic_cube[1][1][4] = 1
semantic_cube[1][2][4] = 1
semantic_cube[1][3][4] = -1
semantic_cube[2][1][4] = 1
semantic_cube[2][2][4] = 1
semantic_cube[2][3][4] = -1
semantic_cube[3][1][4] = -1
semantic_cube[3][2][4] = -1
semantic_cube[3][3][4] = -1

#Equality Operators (== !=)
semantic_cube[1][1][5] = 1
semantic_cube[1][2][5] = 1
semantic_cube[1][3][5] = -1
semantic_cube[2][1][5] = 1
semantic_cube[2][2][5] = 1
semantic_cube[2][3][5] = -1
semantic_cube[3][1][5] = -1
semantic_cube[3][2][5] = -1
semantic_cube[3][3][5] = 3

#Assignation (=)
semantic_cube[1][1][6] = 1
semantic_cube[1][2][6] = 1
semantic_cube[1][3][6] = 1
semantic_cube[2][1][6] = 1
semantic_cube[2][2][6] = 1
semantic_cube[2][3][6] = -1
semantic_cube[3][1][6] = 1
semantic_cube[3][2][6] = -1
semantic_cube[3][3][6] = 1

#Checks the semantic cube and defines the type of result, matching the given input
#Recieves two operands and an operator as parameters, returning a data type
def matchOp(op1, op2, operator):
	return semantic_cube[op1][op2][operator]
