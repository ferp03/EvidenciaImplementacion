#Fernando Pérez García       A01285236
#Luis Blackaller de la Peña  A01178173
#Hervey Navarro Olazarán     A01178086
#Eugenio Garza Cabello       A00836687

import sys
import obten_token as scanner
import http.server
import socketserver

def run_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        print("http://localhost:8000/output.html")
        httpd.serve_forever()

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    global arr
    global count
    if token == tokenEsperado:
        count += 1
        token = arr[count]
    else:
        error(f"token equivocado. Se esperaba {tokenEsperado}, pero se encontró {token}")

# Función principal: implementa el análisis sintáctico
def parser():
    #Borrar la información del documento txt
    f = open("output.html", "w")
    f.write("")

    #Escribir los headers del html
    f = open("output.html", "a")
    f.write("<!DOCTYPE html>\n")
    f.write("<html>\n")
    f.write("<head>\n<title>Output del parser</title>\n</head>\n")
    f.write("<link rel='stylesheet' type='text/css' href='resalta_sintaxis.css'>\n")
    f.write("<body>\n")
    f.write("<div style='display: flex; flex-wrap: wrap;'>\n")
    f.write("<p> \n")
    f.close()

    global token
    global arr 
    global count
    count = 0
    arr = scanner.obten_token() 
    token = arr[count] # inicializa con el primer token
    PROG()
    if token == scanner.END:
        f = open("output.html", "a")
        f.write("<span class='END'>$</span>\n")
        f.write("</p>\n")
        f.write("</div>\n")
        f.write("</body>\n")
        f.write("</html>\n")
        f.close()
        print("Expresion bien construida!!")
        run_server()

#checar si si dejarlo o no, si quiero que se siga corriedndo el servidor aun con el error dejar. 
    else:
        f = open("output.html", "a")
        f.write("<span class='END'>$</span>\n")
        f.write("</p>\n")
        f.write("</body>\n")
        f.write("</html>\n")
        f.close()
        error("ERROR SINTACTICO")
        run_server()

#Funcion que inicializa el programa
#Se reconoce como valido cuando el programa esta conformado por cero o mas expresiones
def PROG():
    while token != scanner.END:
        EXP()

#Funcion que identifica expresiones, las cuales se conforman por atomos o listas
def EXP():
    #Identifica como atomo
    if token == scanner.ID or token == scanner.INT or token == scanner.BOOL or token == scanner.STR:
        ATOMO()
    #Identifica como lista lo que esté entre parentesis
    elif token == scanner.LRP:
        LISTA()

#Funcion que identifica atomos, los cuales pueden ser simbolos o constantes
def ATOMO():
    #Identifica como simbolo
    if token == scanner.ID:
        match(scanner.ID)
    else:
        CONSTANTE()

#Funcion que identifica constantes, las cuales pueden ser enteros, booleanos o strings
def CONSTANTE():
    if token == scanner.INT:
        match(scanner.INT)
    elif token == scanner.BOOL:
        match(scanner.BOOL)
    elif token == scanner.STR:
        match(scanner.STR)

#Funcion que identifica listas, las cuales se conforman por elementos que se encuentran entre parentesis
def LISTA():
    match(scanner.LRP)
    ELEMENTOS()
    match(scanner.RRP)

#Funcion que identifica elementos, los cuales se conforman por cero o mas expresiones
def ELEMENTOS():
    while token in [scanner.ID, scanner.INT, scanner.BOOL, scanner.STR, scanner.LRP]: #Cicla hasta que no sea un parentesis cerrado
        EXP() #Identifica las expresiones

# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)

parser()