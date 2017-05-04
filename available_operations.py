##############################
#                            #
#   Telstar+ Available Ops   #
#                            #
##############################

#List of available operations by the program
#Used in virtual_machine
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
