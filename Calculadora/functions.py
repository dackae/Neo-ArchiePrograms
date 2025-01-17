import math
import os

class functions:
    route = os.path.dirname(os.path.abspath(__file__))
    def operar(self, operacion) -> float:
        try:
            diccionarioFunciones ={
                "sen" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "arcsen" : math.asin,
                "arccos" : math.acos,
                "arctan" : math.atan,
                }
            i=0
            while i < len(operacion):
                if operacion[-i] == '^':
                    operacion = operacion[:-i-1] + [float(operacion[-i-1]) ** float(operacion[-i+1])] + operacion[-i+1:]
                    i-=1
                elif operacion[i] == 'log':
                    try:
                        base = float(operacion[i + 1])
                        numero = float(operacion[i + 2])
                        operacion = operacion[:i] + [math.log(numero, base)] + operacion[i + 3:]
                        i-=1
                    except BaseException:
                        return "Error: No existe el logaritmo de un numero negativo, de 0 ni con una base negativa."
                elif operacion[i] == 'ln':
                    try:
                        numero = float(operacion[i+1])
                        operacion = operacion[:i] + [math.log(numero)] + operacion[i+2:]
                        i-=1
                    except BaseException:
                        return "Eror: No existe el logaritmo de un numero negativo o 0."
                elif operacion[i] == 'root':
                    try:
                        operacion = operacion[:i] + [float(operacion[i + 2])** (1/float(operacion[i + 1]))] + operacion[i + 3:]
                        i-=1
                    except BaseException:
                        return "Error: No se puede hacer una raiz par de un numero negativo."
                elif operacion[i] in diccionarioFunciones:
                    diccionario = diccionarioFunciones[operacion[i]]
                    numero = float(operacion[i + 1])
                    operacion = operacion[:i] + [diccionario(numero)] + operacion[i+2:]
                    i-=1
                i+=1
                #[i+2] es el numero a calcular, [i+1] es la potencia de la raiz

            i=0 #esto es asi por si el usuario poner 2^2^2^2 siempre pillo el ultimo primero
            while i < len(operacion):
                if operacion[i] == '!':
                    try:
                        numero = int((operacion[i -1]))
                        operacion = operacion[:i-1] + [math.factorial(numero)] + operacion[i+1:]
                        i-=1
                    except BaseException:
                        return "Error: No se puede hacer un factorial de un numero negativo, decimal o 0."
                i+=1


            i=0
            while i < len(operacion):
                if operacion[i]=='*':
                    operacion = operacion[:i-1] + [float(operacion[i-1]) * float(operacion[i+1])] + operacion[i+2:]
                    i-=1
                elif operacion[i]=='/':
                    try:
                        operacion = operacion[:i-1] + [float(operacion[i-1]) / float(operacion[i+1])] + operacion[i+2:]
                        i-=1
                    except BaseException:
                        return "Error: No se puede dividir por 0."
                i+=1

            i=0
            while i<len(operacion):
                if operacion[i]=='+':
                    if operacion[0]=='+':
                        operacion = [float(operacion[i+1]) *(1)]
                    operacion = operacion[:i-1] + [float(operacion[i-1]) + float(operacion[i+1])] + operacion[i+2:]
                    i-=1
                elif operacion[i]=='-':
                    if operacion[0]=='-':
                        operacion = [float(operacion[i+1]) *(-1)]
                    else:
                        operacion = operacion[:i-1] + [float(operacion[i-1]) - float(operacion[i+1])] + operacion[i+2:]
                        i-=1
                i+=1

            if len(operacion) > 1:
                raise BaseException
        except BaseException:
            pass
        return operacion[0]

    def ansEscritura(self, respuesta):
        with open(self.route + '/save.txt', 'w') as ans:
            ans.write(str(respuesta))

    def ansLectura(self):
        try:
            with open(self.route + '/save.txt', 'r') as ans:
                return ans.read()
        except BaseException:
            return "Error: No existe ans si nunca has utilizado la calculadora."
