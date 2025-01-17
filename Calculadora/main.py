from separarPorTerminos import separarPorTerminos
from functions import functions

class main:

    #Declaraciones iniciales
    separar = separarPorTerminos()
    fun = functions()
    FIN=False
    INSTRUCCIONES="Bienvenido a la calculadora de Neo-Archie.\nEsta calculadora funciona por terminal, para cerrar la terminal escribe 'x' si necesitas ayuda escribe 'help':"
    AVISO="AVISO: Si vas a poner varios '+' o '-' seguidos, asegurate de poner un parentesis entre estas. Ej: -(-5)\n"
    print(INSTRUCCIONES)
    while FIN==False:
        funcion=input()
        funcion=funcion.lower()
        while funcion=='help':
            print(AVISO)
            print("    + - Suma\n    - - Resta\n    * - Multiplicacion\n    / - Division\n    n^(m) - Exponente de grado m sobre n\n    rootn() - Raiz de grado n\n    sen(n) - Seno de n radianes\n    arcsen(n) - ArcoSeno de n radianes\n    cos(n) - Coseno de n radianes\n    arccos(n) - ArcoCoseno de n radianes\n    tan(n) - Tangente de n radianes\n    arctan(n) - ArcoTangente de n radianes\n    ln(m) - logaritmo neperiano de m\n    logn(m) - logaritmo en base n de m\n    n! - factorial de n\nRecuerda utilizar los parentesis cuando es necesario, el orden de prioridad de una operacion sigue las siglas PEMDAS:\n1. Parentesis\n2. Exponente, loragitmo\n3. Seno, coseno, tangente...\n4. Factorial\n5. Multiplicacion y division\n6. Suma y resta")
            funcion=input()
            funcion=funcion.lower()
        if funcion=='x':
            FIN=True
        else:
            interpretar = separar.interpretar(funcion)

            if interpretar==0:
                resultado=float(funcion)
            else:
                for i in range(len(interpretar)):
                    if interpretar[i]=='ans':
                        interpretar[i]=fun.ansLectura()
                resultado= separar.encontrarParentesisInterno(interpretar)
            fun.ansEscritura(resultado)
            print(f"Resultado: {resultado}\n")