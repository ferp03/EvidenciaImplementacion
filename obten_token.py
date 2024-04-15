#Fernando Pérez A01285236
#Luis Blackaller

import sys

# tokens
INT = 100  # Número entero
FLT = 101  # Número de punto flotante
OPB = 102  # Operador binario
LRP = 103  # Delimitador: paréntesis izquierdo
RRP = 104  # Delimitador: paréntesis derecho
END = 105  # Fin de la entrada
COM = 106  #comas
EQL = 107  #igual
ID = 108  #letra
FUNC = 109 #funcion
ASIG = 110 #asignacion
ERR = 200  # Error léxico: palabra desconocida


# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#      dig  op  (   ) raro esp  .   $   ,    =   ID
MT = [[  1,OPB,LRP,RRP,  4,  0,  4, END, COM, EQL, 5], # edo 0 - estado inicial
      [  1,INT,INT,INT,  4,INT,  2, INT, INT, INT, INT], # edo 1 - dígitos enteros
      [  3,  4,  4,  4,  4,ERR,  4,   4,   4,   4, 4], # edo 2 - primer decimal flotante
      [  3,FLT,FLT,FLT,  4,FLT,  4, FLT, FLT, FLT, 3], # edo 3 - decimales restantes flotante
      [  4,  4,  4,  4,  4,ERR,  4,   4,   4,   4, 4], # edo 4 - estado de error
      [  5, ID, 6, ID,   4,ID,   4,  ID,  ID,  7, 5], # edo 5 - estado de identificador
      [  6, 6,  8, FUNC, 4, 6,   4,  6,   6,   6,  6], #edo 6 - estado de funciones
      [  9, 9,  9, 9,    4, 9,   4,  9,   9,   9,  9], # edo 7 - estado de asignacion
      [  8, 8,  8, FUNC, 4, 8,   4,  8,   8,   8,  8], #edo 8 -  estado de funcion dentro de funcion
      [  9, 9,  9, 9,    4, ASIG,4,  ASIG,9,   9,  9]] #edo 9 - estado de expresiones aritmeticas

# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado
def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c == '0' or c == '1' or c == '2' or \
       c == '3' or c == '4' or c == '5' or \
       c == '6' or c == '7' or c == '8' or c == '9': # dígitos
        return 0
    elif c == '+' or c == '-' or c == '*' or \
         c == '/': # operadores
        return 1
    elif c == '(': # delimitador (
        return 2
    elif c == ')': # delimitador )
        return 3
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 5
    elif c == '.': # punto
        return 6
    elif c == '$': # fin de entrada
        return 7
    elif c  == ",": #comas
        return 8
    elif c == '=': #igual
        return 9
    elif c.isalpha() or c == '_': #identificadores
        return 10
    else: # caracter raro
        return 4

_c = None    # siguiente caracter
_leer = True # indica si se requiere leer un caracter de la entrada estándar

# Función principal: implementa el análisis léxico
def obten_token():
    # Abrir el archivo txt
    f = open("output.txt", "a")
    f.write("<body>\n")

    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    global _c, _leer
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    ARR_TOKENS = []
    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if _leer: _c = sys.stdin.read(1)
            else: _leer = True
            edo = MT[edo][filtro(_c)]
            if edo < 100 and edo != 0: lexema += _c
            #Si hay una funcion dentro de otra funcion
            if edo == 8:
                while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
                    if _leer: _c = sys.stdin.read(1)
                    else: _leer = True
                    edo = MT[edo][filtro(_c)]
                    if edo < 100 and edo != 0: lexema += _c
                    if edo == 109:
                        edo = 6
                        lexema += _c
                        break
        if edo == INT:    
            _leer = False # ya se leyó el siguiente caracter
            f.write(f"<p>Entero {lexema}</p>\n")
            ARR_TOKENS.append(INT)
        elif edo == FLT:   
            _leer = False # ya se leyó el siguiente caracter
            f.write(f"<p>Flotante {lexema}</p>\n")
            ARR_TOKENS.append(FLT)
        elif edo == OPB:   
            lexema += _c  # el último caracter forma el lexema
            f.write(f"<p>Operador {lexema}</p>\n")
            ARR_TOKENS.append(OPB)
        elif edo == LRP:   
            lexema += _c  # el último caracter forma el lexema
            f.write(f"<p>Delimitador {lexema}</p>\n")
            ARR_TOKENS.append(LRP)
        elif edo == RRP:  
            lexema += _c  # el último caracter forma el lexema
            f.write(f"<p>Delimitador {lexema}</p>\n")
            ARR_TOKENS.append(RRP)
        elif edo == COM:
            lexema += _c
            f.write(f"<p>Separador ,</p>\n")
            ARR_TOKENS.append(COM)
        elif edo == EQL:
            lexema += _c
            f.write(f"<p>Igual =</p>\n")
            ARR_TOKENS.append(EQL)
        elif edo == ID:
            _leer = False
            f.write(f"<p>Identificador {lexema}</p>\n")
            ARR_TOKENS.append(ID)
        elif edo == FUNC:
            lexema += _c
            f.write(f"<p>Funcion {lexema}</p>\n")
            ARR_TOKENS.append(FUNC)  
        elif edo == ASIG:
            lexema += _c
            f.write(f"<p>Asignacion {lexema}</p>\n")
            ARR_TOKENS.append(ASIG)  
        elif edo == END:
            print("Fin de expresion")
            ARR_TOKENS.append(END)
            f.close()
            return ARR_TOKENS
        else:   
            _leer = False # el último caracter no es raro
            f.write(f"<h2>ERROR! palabra ilegal {lexema}</h2>\n")
            ARR_TOKENS.append(ERR)
            return ARR_TOKENS
        lexema = ""
        edo = 0
