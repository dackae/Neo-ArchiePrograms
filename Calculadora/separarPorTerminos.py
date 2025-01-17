import re
import functions

class separarPorTerminos:
    
    def interpretar(self, funcion):
        #fin del def
        #web donde veo como hacer la expresion: pythex.org
        if funcion.isdigit()==True:
            return 0
        else:
            splitter= r'(\(|\)|\-|\+|\/|\*|\^|\!|root|log|\d+(\.\d+)?|\b(?:sen|arcsen|cos|arccos|tan|arctan|ln|ans)\b)'
            funcionSeparada=funcion
            funcionSeparada=re.findall(splitter, funcionSeparada)
            funcionSeparada= [x[0] if isinstance(x, tuple) 
                              else x 
                              for x in funcionSeparada]
        return funcionSeparada
    #(sen(root2(13*(4+3)*5))+2.5*3!)/(2)+2^2+ln(3)+log10(10)

    #Para encontrar parentesis, tanto basicos como sen, cos, rootn...
    def encontrarParentesisInterno(self, funcionSeparada):
        try:
            funciones= functions.functions()
            if funcionSeparada==[]:
                return 0
            ListaIndiceParentesis = []
            resultado=0
            for i, item in enumerate(funcionSeparada): #Creo 1 indice asi puedo usar la lista a la que le voy a anyadir la segunda variable creada "item" que recorre "funcionSeparada"
                if item == "(":
                    ListaIndiceParentesis.append(i)
                elif item == ")":
                    ParentesisAbierto = ListaIndiceParentesis.pop()
                    subOperacion = funcionSeparada[ParentesisAbierto+1:i]
                    resultado = funciones.operar(subOperacion)
                    funcionSeparada = funcionSeparada[:ParentesisAbierto] + [resultado] + funcionSeparada[i+1:]
                    return self.encontrarParentesisInterno(funcionSeparada)
            resultado = funciones.operar(funcionSeparada)
        except BaseException as e:
            return "Error: Si ves un error aqui, has hecho algo MUY mal"
        return resultado