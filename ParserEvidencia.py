# Autor: Fernando Pérez

import sys
import obten_token as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        token = scanner.obten_token()
    else:
        error("token equivocado")

# Función principal: implementa el análisis sintáctico
def parser():
    global token
    arr = scanner.obten_token() 
    token = arr[-1] # inicializa con el primer token
    EXP()
    if token == scanner.END:
        print("Expresion bien construida!!")
    else:
        error("expresion mal terminada")

# Reconoce estructuras SEN
def SEN():
    if token == scanner.ID:
        match(scanner.ID)
        SEN1()

def SEN1():
    if token == scanner.LRP:
        match(scanner.LRP)
        ARGS()
        match(scanner.RRP)
    elif token == scanner.ID:
        match(scanner.ID)
        EXP()

#Reconoce expresiones
def EXP():
    if token in [scanner.INT, scanner.FLT]:
        match(token)
        EXP1()
    elif token == scanner.ID:
        match(scanner.ID)
        ID1()
        EXP1()
    elif token == scanner.LRP:
        match(scanner.LRP)
        EXP()
        match(scanner.RRP)
        EXP1()

def EXP1():
    if token in [scanner.OPB, scanner.EQL]:
        match(token)
        EXP()
        EXP1()

#Maneja argumentos
def ARGS():
    if token != scanner.RRP:
        EXP()
        ARGS1()

def ARGS1():
    if token == scanner.COM:
        match(scanner.COM)
        EXP()
        ARGS1()

def ID1():
    if token == scanner.LRP:
        match(scanner.LRP)
        ARGS()
        match(scanner.RRP)


# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)

parser()