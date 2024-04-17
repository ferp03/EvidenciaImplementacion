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
    EXP()
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