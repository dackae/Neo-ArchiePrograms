import curses
import subprocess
import os

e = ""

# Ruta donde creare un bash
route = os.path.dirname(os.path.abspath(__file__))

# Funcion que maneja la logica de seleccion y completado de texto
def interfaz_interactiva(stdscr):
    curses.curs_set(1)  # Mostrar el cursor
    stdscr.clear()  # Limpiar la pantalla

    # Opciones para el primer paso + crear hueco en las respuestas
    # Despues de Tipo de dat va "Tamanyo", pero todavia no funciona
    opciones = ["Ruta de busqueda", "Nombre del archivo, directorio...", "Extension", "Tipo de dato", "Tamanyo", "Tiempo desde la ultima edicion", "Permisos", "He terminado", "Ayuda"]
    seleccion = 0
    respuestas = []
    for i in range(0, len(opciones)-1):
        respuestas.append(None)

    # Sublista de opciones para "seleccionar tipo de dato"
    opcionesTipoDato = [
        "Archivos", "Directorio", "Enlace simbolico",
        "Dispositivos de caracteres", "Dispositivos de bloque",
        "Tuberias nombradas", "Zocalo", "Eliminar respuesta anterior"
    ]
    
    diccionarioTipoDato = {
        "Archivos" : "f",
        "Directorio" : "d",
        "Enlace simbolico" : "l",
        "Dispositivos de caracteres" : "c",
        "Dispositivos de bloque" : "b",
        "Tuberias nombradas" : "p",
        "Zocalo" : "s"
    }
    
    opcionesTamanio = [
        "Tamanyo exacto", "Tamanyo superior a", "Tamanyo inferior a", "Indicar un rango", "Eliminar respuesta anterior"
    ]
    dicMultiplicadorTamanyo = {
        "c" : 1,
        "b" : 512,
        "k" : 1024,
        "M" : 1024*1024,
        "G" : 1024*1024*1024
    }

    finBucleGeneral=False
    while finBucleGeneral==False:
        stdscr.clear()
        stdscr.addstr(0, 0, "Seleccione una opcion (usando flechas y Enter):")
        for i, opcion in enumerate(opciones):
        
            if i == seleccion:
                stdscr.addstr(3 + i, 2, f"> {opcion}", curses.A_REVERSE)
            else:
                stdscr.addstr(3 + i, 2, f"  {opcion}")
        
            if i != len(opciones)-1:
                if opciones[i] == "Tamanyo" and respuestas[i] is not None: # Muestra la respuesta guardada sin convertir el tamanyo
                    stdscr.addstr(3 + i, 40, f"[{rango1}, {rango2}]")
                if respuestas[i] is not None: # Muestra la respuesta guardada
                    stdscr.addstr(3 + i, 40, f"[{respuestas[i]}]")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == curses.KEY_DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == 27:
            finBucleGeneral = True
        elif key == 10:  # Enter
            if opciones[seleccion] == "He terminado":
                if respuestas[1] is None:
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Error: El nombre debe ser introducido antes de finalizar.")
                    stdscr.refresh()
                    stdscr.getch()  # Esperar la tecla para continuar
                else:
                    finBucleGeneral=True # Si la ruta esta completa, salir

            else:
                # Si la opcion seleccionada es "seleccionar tipo de dato"
                if opciones[seleccion] == "Tipo de dato":
                    subseleccion=0
                    finBucleTipoDato=False
                    while finBucleTipoDato==False:
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Selecciona un tipo de dato (usando flechas y Enter):")
                     
                        for i, subopcion in enumerate(opcionesTipoDato):
                            if i == subseleccion:
                                stdscr.addstr(2 + i, 2, f"> {subopcion}", curses.A_REVERSE)
                            else:
                                stdscr.addstr(2 + i, 2, f"  {subopcion}")

                        stdscr.refresh()
                        key_sub = stdscr.getch()

                        # Navegar por las opcionesTipoDato
                        if key_sub == curses.KEY_UP:
                            subseleccion = (subseleccion - 1) % len(opcionesTipoDato)
                        elif key_sub == curses.KEY_DOWN:
                            subseleccion = (subseleccion + 1) % len(opcionesTipoDato)
                        elif key_sub == 10:
                            respuestas[seleccion] = opcionesTipoDato[subseleccion]
                            if opcionesTipoDato[subseleccion] == "Eliminar respuesta anterior":
                                respuestas[seleccion] = None
                            finBucleTipoDato=True
                        elif key_sub ==27:
                            finBucleTipoDato=True

                elif opciones[seleccion]=="Extension":
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Indica la extension del archivo:")
                    stdscr.refresh()
                    curses.echo()
                    extension = stdscr.getstr(2, 0, 40).decode("utf-8") # Guardar respuesta
                    if extension != '' and extension[0] != ".":
                        extension = "." + extension
                    respuestas[seleccion] = extension
                    if respuestas[seleccion] == '':
                        respuestas[seleccion] = None
                    curses.noecho()

                elif opciones[seleccion] == "Tamanyo":
                    finBucleTamanyo=False
                    subseleccion=0
                    while finBucleTamanyo==False:
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Indica el simbolo, el tamanyo y la unidad (c (Bytes), b (512-bytes block), k, M, G):")
                    
                        for i, subopcion in enumerate(opcionesTamanio):
                            if i == subseleccion:
                                stdscr.addstr(3 + i, 2, f"> {subopcion}", curses.A_REVERSE)
                            else:
                                stdscr.addstr(3 + i, 2, f"  {subopcion}")

                        stdscr.refresh()
                        key_sub = stdscr.getch()

                        # Navegar por las opcionesTamanio
                        if key_sub == curses.KEY_UP:
                            subseleccion = (subseleccion - 1) % len(opcionesTamanio)
                        elif key_sub == curses.KEY_DOWN:
                            subseleccion = (subseleccion + 1) % len(opcionesTamanio)
                        elif key_sub == 10:
                            stdscr.clear()
                            stdscr.addstr(0, 0, f"Indica el tamanyo (se convertira automaticamente a bytes (c)):")
                            stdscr.refresh()
                            if opcionesTamanio[subseleccion] == "Tamanyo exacto":
                                curses.echo()
                                respuestas[seleccion] = stdscr.getstr(2, 0, 40).decode("utf-8") # Guardar respuesta
                                curses.noecho()
                            elif opcionesTamanio[subseleccion] == "Tamanyo superior a":
                                curses.echo()
                                respuestas[seleccion] = '+' + stdscr.getstr(2, 0, 40).decode("utf-8") # Guardar respuesta
                                curses.noecho()
                            elif opcionesTamanio[subseleccion] == "Tamanyo inferior a":
                                curses.echo()
                                respuestas[seleccion] = '-' + stdscr.getstr(2, 0, 40).decode("utf-8") # Guardar respuesta
                                curses.noecho()
                            elif opcionesTamanio[subseleccion] == "Indicar un rango":
                                try:
                                    stdscr.addstr(2, 0, "1r Numero:")
                                    stdscr.addstr(3, 0, "2do Numero:")
                                    stdscr.refresh()
                                    curses.echo()
                                    rango1 = stdscr.getstr(2, 11, 40).decode("utf-8") # Guardar 1r numero
                                    curses.noecho()
                                    curses.echo()
                                    rango2 = stdscr.getstr(3, 12, 40).decode("utf-8") # Guardar 2do numero
                                    curses.noecho()
                                    # Convertir a numero para ver cual es mayor
                                    rango1 = rango1.replace(" ", "")
                                    rango1Numeral = int((rango1[:len(rango1)-1])) * dicMultiplicadorTamanyo[rango1[-1]]
                                    rango2 = rango2.replace(" ", "")
                                    rango2Numeral = int((rango2[:len(rango2)-1])) * dicMultiplicadorTamanyo[rango2[-1]]
                                    rango1 = rango1[:-1]
                                    rango2 = rango1[:-1]
                                    if rango1Numeral > rango2Numeral: # Cambiar posiciones
                                        aux = rango1
                                        rango1 = rango2
                                        rango2 = aux
                                    rango1 = '+' + str(rango1Numeral) + 'c'
                                    rango2 = '-' + str(rango2Numeral) + 'c'
                                    respuestaRango = rango1, '-size', rango2 # Guardar respuesta                                    
                                    respuestas[seleccion] = " ".join(respuestaRango)
                                except BaseException:
                                    stdscr.clear()
                                    stdscr.addstr(0, 0, "Asegurate de haber escrito bien los numeros y las unidades.")
                                    stdscr.refresh()
                                    stdscr.getch()
                            finBucleTamanyo=True
                            if respuestas[seleccion] == '' or opcionesTamanio[subseleccion] == "Eliminar respuesta anterior":
                                respuestas[seleccion] = None
                                finBucleTamanyo=True
                        if key_sub ==27:
                            finBucleTamanyo=True

                elif opciones[seleccion]=="Permisos":
                    try:
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Indica los permisos del archivo:")
                        stdscr.refresh()
                        curses.echo()
                        respuestaPermisos = stdscr.getstr(2, 0, 40)
                        respuestas[seleccion] = respuestaPermisos.decode("utf-8") # Guardar respuesta
                        curses.noecho()
                        try:
                            respuestaInt = int(respuestaPermisos)
                        except:
                            if  respuestas[seleccion] != '':
                                stdscr.clear()
                                stdscr.addstr(0, 0, "Asegurate de que hayas introducido solo numeros.")
                                stdscr.refresh()
                            respuestas[seleccion] = None
                            stdscr.getch()

                    except BaseException:
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Asegurate de que hayas introducido los datos correctamente.")
                        stdscr.refresh()
                        stdscr.getch()

                elif opciones[seleccion] == "Ayuda":
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Para salir de un submenu (como este) presiona Esc.\nPara descartar una de tus respuestas en un submenu selecciona 'Eliminar respuesta anterior'.\nPara descartar una respuesta por entrada de texto presiona Enter sin introducir texto.")
                    stdscr.refresh()
                    finAyuda = False
                    while finAyuda==False:
                        salidaAyuda = stdscr.getch()
                        if salidaAyuda == 27:
                            finAyuda=True

                else:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Indica el valor de {opciones[seleccion]}:")
                    stdscr.refresh()
                    curses.echo()
                    respuestas[seleccion] =  stdscr.getstr(2, 0, 40).decode("utf-8")  # Guardar respuesta
                    if respuestas[seleccion] == '':
                        respuestas[seleccion] = None
                    curses.noecho()

    # Guardar el resultado final
    final_text=["find"]
    for i, opcion in enumerate(opciones):
        if i == len(opciones)-1:
            pass
        elif respuestas[i] is not None:
            if opciones[i]== "Ruta de busqueda":
                final_text.append(respuestas[i])
            elif opciones[i]== "Nombre del archivo, directorio...":
                nombreArchivo = (f"\"{respuestas[i]}")
                if respuestas[i+1] is None:
                    final_text.extend(["-name", f"\"{respuestas[i]}\""])
            elif opciones[i]== "Extension":
                if opciones[i+1] is not None:
                    if respuestas[i+1]=="Archivos":
                        final_text.extend(["-name", f"{nombreArchivo}{respuestas[i]}\""])
                    else:
                        pass
            elif opciones[i]== "Tipo de dato":
                final_text.extend(["-type", diccionarioTipoDato.get(respuestas[i])])
            elif opciones[i]== "Tamanyo":
                final_text.extend(["-size", respuestas[i]])
            elif opciones[i]== "Tiempo desde la ultima edicion":
                final_text.extend(["-mtime", respuestas[i]])
            elif opciones[i]=="Permisos":
                final_text.extend(["-perm", respuestas[i]])

    try:
        stdscr.clear()
        if final_text != ["find"]:
            fin="Resultado final de la busqueda: "
            final_text_joined = " ".join(final_text)
            stdscr.addstr(0, 0, fin+ final_text_joined)
            stdscr.refresh()
            stdscr.getch()  # Esperar la tecla de salida final_text


    except BaseException:
        ERROR="Ha ocurrido un error, asegurate de que hayas proporcionado correctamente los datos."
        stdscr.addstr(0, 0, ERROR)
        stdscr.refresh()
        stdscr.getch()
    if final_text != ["find"]:
        with open(route + "/ejecucion.sh", 'w') as e:
            e.write(final_text_joined)


# Inicializar curses y ejecutar el programa
resultat = curses.wrapper(interfaz_interactiva)

try:
    if os.path.isfile(route + "/ejecucion.sh"): # Revisa que exista el .bash
        subprocess.run(['bash', route + '/ejecucion.sh'], text=True)
except BaseException:
    print("Algo ha salido mal, si este error perdura, contacta con: urosal@institutmvm.cat")