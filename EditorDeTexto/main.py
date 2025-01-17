import curses
import os
import time

def main(stdscr):
    # Configurar la terminal
    curses.curs_set(1)  # Mostrar cursor
    stdscr.keypad(True)  # Activar teclas especiales
    curses.noecho()  # Desactivar eco de teclas
    
    # Variables iniciales
    cursorMenu = 0
    text = []  # Almacenara lineas de texto
    cursorLinea=0
    cursorCaracter=0
    routeEditor = os.path.dirname(os.path.abspath(__file__)) + '/textos'
    routeTextos = os.path.dirname(os.path.abspath(__file__)) + '/textos/'

    # Bucle principal
    while True:
        if os.path.isdir(routeEditor) == False: # Revisa la existencia de un directorio 'textos'
            os.makedirs(routeEditor)
        menu = ["Nuevo Archivo"]  # Almacenara opciones de distintos '.txt'
        for textFile in os.listdir(os.path.relpath(routeTextos)):
            if textFile.endswith('.txt'):
                menu.insert(-2, textFile)

        stdscr.clear()
        stdscr.addstr(1, 0, "Seleccione un archivo (usando flechas y Enter para editar, ESC para salir):")
        for i, file in enumerate(menu):
            if i == cursorMenu:
                stdscr.addstr(4 + i, 2, f"> {file}", curses.A_REVERSE)
            else:
                stdscr.addstr(4 + i, 2, f"  {file}")
        stdscr.refresh()

        keyMenu = stdscr.getch()

        if keyMenu==27:
            break
        if keyMenu == curses.KEY_UP: # Cursor hacia arriba
            cursorMenu = (cursorMenu - 1) % len(menu)
        elif keyMenu == curses.KEY_DOWN: # Cursor hacia abajo
            cursorMenu = (cursorMenu + 1) % len(menu)
        elif keyMenu == 10:
            text=[]
            if os.path.isdir(routeTextos): # Revisa la existencia de un directorio 'textos' por si el usuario lo borra
                if os.path.isfile(routeTextos+menu[cursorMenu]): # Revisa que exista el .txt
                    with open(routeTextos+menu[cursorMenu], 'r') as save: # Abre dicho .txt y lo lee
                        for linea in save:
                            text.append(linea.strip())

            writingFile=True
            cursorLinea=0
            cursorCaracter=0
            while writingFile==True:
                sizeTerminal = stdscr.getmaxyx()
                sizeTerminalX = sizeTerminal[1]
                sizeTerminalY = sizeTerminal[0]
                cursorLinea = cursorLinea % sizeTerminalY

                if len(text) == 0:  # Si el texto esta vacio, inicializa una nueva linea (si esto no esta te fallara la flecha derecha y el enter)
                    text.append('')
                stdscr.clear()
                for numLinea, linea in enumerate(text):
                    stdscr.addstr(numLinea, 0, linea)  # Mostrara el texto linea por linea
                stdscr.move(cursorLinea, cursorCaracter)
                stdscr.refresh()
                key = stdscr.getch()

                if key == 27:  # ESC para salir
                    writingFile=False
                elif key in (curses.KEY_BACKSPACE, 127):  # Eliminar caracteres
                    if cursorCaracter > 0:
                        linea = text[cursorLinea]
                        text[cursorLinea] = linea[:cursorCaracter - 1] + linea[cursorCaracter:]
                        cursorCaracter -= 1
                    elif cursorLinea > 0:  # Elimina lineas vacias
                        cursorCaracter = len(text[cursorLinea - 1])
#region -- Codigo pendiente de arreglar
# Forma parte de una posible solucion a el anyadir mas texto de lo que la terminal puede

                        # if len(text[cursorLinea]) == sizeTerminalX: 
                        #     cursorCaracter-=1
#endregion
                        text[cursorLinea - 1] += text[cursorLinea]
                        text.pop(cursorLinea)
                        cursorLinea -= 1
#region -- Codigo pendiente de arreglar
# Forma parte de una posible solucion a el anyadir mas texto de lo que la terminal puede
                    # elif '\n' in text[cursorLinea]: 
                    #     text[cursorLinea].pop('\n')
#endregion
                elif key == curses.KEY_DC:
                    linea = text[cursorLinea]
                    if cursorCaracter < len(linea):
                        text[cursorLinea] = linea[:cursorCaracter] + linea[cursorCaracter + 1:]
                    elif cursorLinea != len(text)-1:
                        lineaAbajo = text[cursorLinea + 1]
                        linea += lineaAbajo
                        text[cursorLinea] = linea
                        text.pop(cursorLinea + 1)
                        cursorCaracter = cursorCaracter % len(linea)
                elif key == curses.KEY_DOWN:  # Cursor hacia abajo
                    if cursorLinea < len(text) - 1:
                        cursorLinea += 1
                        cursorCaracter = min(cursorCaracter, len(text[cursorLinea]))
                elif key == curses.KEY_UP:  # Cursor hacia arriba
                    if cursorLinea > 0:
                        cursorLinea -= 1
                        cursorCaracter = min(cursorCaracter, len(text[cursorLinea]))
                elif key == curses.KEY_LEFT:  # Cursor a la izquierda
                    if cursorCaracter > 0:
                        cursorCaracter -= 1
                    elif cursorLinea > 0:
                        cursorLinea -= 1
                        cursorCaracter = len(text[cursorLinea])
                        if len(text[cursorLinea]) >= sizeTerminalX:
                            cursorCaracter-=1
                elif key == curses.KEY_RIGHT:  # Cursor a la derecha
                    if cursorCaracter == sizeTerminalX-1:
                        if cursorLinea < len(text):
                            cursorLinea += 1
                            cursorCaracter = 0
                    elif cursorCaracter < len(text[cursorLinea]):
                        cursorCaracter += 1
                    elif cursorLinea < len(text) - 1:
                        cursorLinea += 1
                        cursorCaracter = 0
#region -- Codigo pendiente de arreglar
                    # elif cursorLinea < len(text) - 1 and cursorCaracter > sizeTerminalX:
                    #     cursorCaracter = cursorCaracter % sizeTerminalX
#endregion
                elif key == curses.KEY_ENTER or key == 10:  #Enter para nueva linea
                    linea = text[cursorLinea]
                    nueva_linea = linea[cursorCaracter:]
                    text[cursorLinea] = linea[:cursorCaracter]
                    text.insert(cursorLinea + 1, nueva_linea)
                    cursorLinea += 1

                    if len(text) > sizeTerminalY or cursorLinea > sizeTerminalY:
                        stdscr.clear()
                        stdscr.addstr(1, 0, "Has alcanzado el limite de lineas de este archivo")
                        stdscr.refresh()
                        time.sleep(1) # Sleep para evitar cambiar de texto a aviso muy rapidamente
                        cursorLinea-=1
                        text[cursorLinea] = linea
                        text.pop(cursorLinea + 1)
                    else:
                        cursorCaracter = 0

                else:  # Inserta texto
                    linea = text[cursorLinea]
                    sizeText = len(text[cursorLinea])

                    # if len(text[cursorLinea]) > sizeTerminalX: # ESTO ES UNA PSOBILE SOLUCION AL PROBLEMA DE AnyADIR LINEAS QUE FORMAN PARTE DE UNA LINEA ANTERIOR
                    #     text.insert(cursorLinea + 1, '')
                    # if len(text[cursorLinea]) > sizeTerminalX: # lo mismo
                    #     text[cursorLinea] = linea[:sizeTerminalX] + '\n' + linea[sizeTerminalX:]

                    char = chr(key)
                    if len(text) == 0:
                        text.append('')
                    text[cursorLinea] = linea[:cursorCaracter] + char + linea[cursorCaracter:]
                    cursorCaracter += 1

                    if sizeText == sizeTerminalX or cursorCaracter == sizeTerminalX:
                        text[cursorLinea] = linea[:sizeText]
                        cursorCaracter-=1
                        stdscr.clear()
                        stdscr.addstr(1, 0, "Has alcanzado el limite de caracteres en esta linea")
                        stdscr.refresh()
                        time.sleep(1)




            # Al salir con 'ESC' guardar o no
            stdscr.clear()
            stdscr.addstr(1, 0, "¿Quieres guardar el archivo? (S) (N):")
            stdscr.refresh()
            saveOrNot = False
            while saveOrNot==False:
                keySave = stdscr.getch()
                if keySave==19 or keySave==115: # Tecla s
                    if menu[cursorMenu]=="Nuevo Archivo":
                        try:
                            fileSaved=False
                            while fileSaved==False:
                                stdscr.clear()
                                stdscr.addstr(1, 0, "Ponle un nombre al archivo:")
                                stdscr.refresh()
                                curses.echo()
                                archivoAGuardar = stdscr.getstr(2, 0, 40).decode("utf-8") + '.txt'
                                curses.noecho()
                                if archivoAGuardar != os.path.isfile(routeTextos+archivoAGuardar):
                                    with open(routeTextos+archivoAGuardar, 'w') as save:
                                        text= '\n'.join(text)
                                        save.write(text)
                                    fileSaved=True
                                else:
                                    stdscr.clear()
                                    stdscr.addstr(1, 0, "Ya existe un archivo con ese nombre")
                                    stdscr.refresh()

                        except BaseException:
                            stdscr.clear()
                            stdscr.addstr(1, 0, "Asegurate de escribir un nombre de archivo valido.")
                            stdscr.refresh()

                    else:
                        with open(routeTextos+menu[cursorMenu], 'w') as save:
                            text= '\n'.join(text)
                            save.write(text)
                    saveOrNot = True
                elif keySave==10 or keySave==27 or keySave==110: # Tecla n
                    saveOrNot = True


if __name__ == "__main__":
   curses.wrapper(main)