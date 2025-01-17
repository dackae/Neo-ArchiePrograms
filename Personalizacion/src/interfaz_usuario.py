import curses
import time
from typing import List
from src import Personalizacion
from .constantes import *

class InterfazUsuario:
    def __init__(self, stdscr, personalizacion: Personalizacion):
        try:
            self.stdscr = stdscr
            self.personalizacion = personalizacion
            self.seleccion_actual_izquierda = 0
            self.seleccion_actual_derecha = 0
            self.columna_actual = 0
            self.altura = 40
            self.ancho = 78
        except Exception as e:
            print(f"Error al inicializar InterfazUsuario: {e}")
            raise

    def dibujar_ventana_bordeada(self, inicio_y: int, inicio_x: int, altura: int, ancho: int, titulo: str):
        try:
            self.stdscr.addstr(inicio_y, inicio_x, titulo)
            self.stdscr.attron(curses.color_pair(1))
            for y in range(altura):
                self.stdscr.addstr(inicio_y + y, inicio_x, '│')
                self.stdscr.addstr(inicio_y + y, inicio_x + ancho - 1, '│')
            self.stdscr.addstr(inicio_y, inicio_x, '┌' + '─' * (ancho - 2) + '┐')
            self.stdscr.addstr(inicio_y + altura - 1, inicio_x, '└' + '─' * (ancho - 2) + '┘')
            self.stdscr.attroff(curses.color_pair(1))
        except curses.error as e:
            print(f"Error al dibujar la ventana: {e}")

    def entrada_emergente(self, prompt: str) -> str:
        try:
            max_y, max_x = self.stdscr.getmaxyx()
            altura, ancho = 3, len(prompt) + 10
            inicio_y, inicio_x = (max_y - altura) // 2, (max_x - ancho) // 2

            self.dibujar_ventana_bordeada(inicio_y, inicio_x, altura, ancho, TITULO_ENTRADA)
            self.stdscr.addstr(inicio_y + 1, inicio_x + 5, prompt)
            
            curses.echo()
            entrada_str = self.stdscr.getstr(inicio_y + 1, inicio_x + len(prompt) + 5).decode('utf-8')
            curses.noecho()
            
            return entrada_str
        except Exception as e:
            print(f"Error en entrada_emergente: {e}")
            return ""

    def dibujar_opciones(self, opciones: List[str], inicio_x: int, esta_activa: bool):
        try:
            max_y, _ = self.stdscr.getmaxyx()
            for idx, opcion in enumerate(opciones):
                if idx == (self.seleccion_actual_izquierda if esta_activa else self.seleccion_actual_derecha) and esta_activa == (self.columna_actual == 0):
                    self.stdscr.addstr((max_y - self.altura) // 2 + idx + 1, inicio_x + 1, opcion, curses.A_REVERSE)
                else:
                    self.stdscr.addstr((max_y - self.altura) // 2 + idx + 1, inicio_x + 1, opcion)
        except curses.error as e:
            print(f"Error al dibujar opciones: {e}")

    def dibujar_descripcion(self, descripcion: str, inicio_y: int, inicio_x: int):
        try:
            ancho_maximo = self.ancho - 40
            altura_maxima = self.altura - inicio_y + 20000

            palabras = descripcion.split()
            lineas = []
            linea_actual = []
            longitud_actual = 0
            for palabra in palabras:
                if longitud_actual + len(palabra) + 1 <= ancho_maximo:
                    linea_actual.append(palabra)
                    longitud_actual += len(palabra) + 1
                else:
                    lineas.append(' '.join(linea_actual))
                    linea_actual = [palabra]
                    longitud_actual = len(palabra)
            if linea_actual:
                lineas.append(' '.join(linea_actual))

            lineas = lineas[:altura_maxima]

            for idx, linea in enumerate(lineas):
                if inicio_y + idx < self.altura + 20000:
                    self.stdscr.addstr(inicio_y + idx, inicio_x, linea[:ancho_maximo], curses.color_pair(2))
        except curses.error as e:
            print(f"Error al dibujar descripcion: {e}")

    def mostrar_ayuda(self):
        max_y, max_x = self.stdscr.getmaxyx()
        altura_ayuda = min(len(TEXTO_AYUDA) + 2, max_y - 10)
        ancho_ayuda = min(self.ancho - 2, max_x - 10)

        inicio_y_ayuda = (max_y - altura_ayuda) // 2
        inicio_x_ayuda = (max_x - ancho_ayuda) // 2

        ventana_ayuda = curses.newwin(altura_ayuda, ancho_ayuda, inicio_y_ayuda, inicio_x_ayuda)
        ventana_ayuda.box()
        ventana_ayuda.addstr(0, 2, TITULO_AYUDA)

        for idx, linea in enumerate(TEXTO_AYUDA[:altura_ayuda - 2]):
            ventana_ayuda.addstr(idx + 1, 1, linea)
        
        ventana_ayuda.refresh()
        self.stdscr.getch()

    def bucle_principal(self):
        try:
            curses.curs_set(0)
            curses.start_color()
            curses.init_pair(1, COLOR_FONDO, COLOR_TEXTO)
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
            mostrar_ayuda = False
    
            while True:
                self.stdscr.clear()
                max_y, max_x = self.stdscr.getmaxyx()
    
                if max_y < ALTURA_MINIMA or max_x < ANCHO_MINIMO:
                    self.stdscr.addstr(max_y // 2, max_x // 2 - 20, MENSAJE_PANTALLA_PEQUENA)
                    self.stdscr.refresh()
                    self.stdscr.getch()
                    continue
    
                ancho_ventana = min(max_x // 2 - 5, 40)
                altura_ventana = min(max_y - 10, 40)
    
                inicio_x_izquierda = (max_x - (ancho_ventana * 2 + 10)) // 2
                inicio_x_derecha = inicio_x_izquierda + ancho_ventana + 10
                inicio_y = (max_y - altura_ventana) // 2
    
                self.dibujar_ventana_bordeada(inicio_y, inicio_x_izquierda, altura_ventana, ancho_ventana, TITULO_COLUMNA_IZQUIERDA)
                self.dibujar_ventana_bordeada(inicio_y, inicio_x_derecha, altura_ventana, ancho_ventana, TITULO_COLUMNA_DERECHA)
    
                apartados = self.personalizacion.apartados
                opciones_izquierda = [f">> {a.nombre}" for a in apartados]
                
                espacio_por_apartado = 2
                altura_total_apartados = len(opciones_izquierda) * espacio_por_apartado
                
                inicio_y_izquierda = inicio_y + (altura_ventana - altura_total_apartados) // 2
    
                for idx in range(len(opciones_izquierda)):
                    y_apartado = inicio_y_izquierda + idx * espacio_por_apartado
                    
                    if idx == self.seleccion_actual_izquierda:
                        self.stdscr.addstr(y_apartado, inicio_x_izquierda + 1, opciones_izquierda[idx], curses.A_REVERSE)
                    else:
                        self.stdscr.addstr(y_apartado, inicio_x_izquierda + 1, opciones_izquierda[idx])
    
                if self.seleccion_actual_izquierda < len(apartados):
                    apartado_seleccionado = apartados[self.seleccion_actual_izquierda]
                    subapartados = self.personalizacion.obtener_subapartados_para_apartado(apartado_seleccionado.identidad)
                    opciones_derecha = [f">> {s.nombre}" for s in subapartados]
    
                    espacio_por_subapartado = 3
    
                    for idx in range(len(opciones_derecha)):
                        y_subapartado = inicio_y + idx * espacio_por_subapartado + 1
                        
                        if idx == self.seleccion_actual_derecha and self.columna_actual == 1:
                            self.stdscr.addstr(y_subapartado, inicio_x_derecha + 1, opciones_derecha[idx], curses.A_REVERSE)
                        else:
                            if y_subapartado < inicio_y + altura_ventana: 
                                self.stdscr.addstr(y_subapartado, inicio_x_derecha + 1, opciones_derecha[idx])
    
                    inicio_y_descripcion = inicio_y + altura_ventana - 5
                    if self.seleccion_actual_derecha < len(subapartados):
                        subapartado_seleccionado = subapartados[self.seleccion_actual_derecha]
                        texto_descripcion = subapartado_seleccionado.descripcion
                        
                        palabras = texto_descripcion.split()
                        lineas = []
                        linea_actual = ""
                        
                        for palabra in palabras:
                            if len(linea_actual) + len(palabra) + 1 > (ancho_ventana - 4):
                                lineas.append(linea_actual)
                                linea_actual = palabra
                            else:
                                linea_actual += " " + palabra if linea_actual else palabra
                        
                        if linea_actual:
                            lineas.append(linea_actual)
    
                        for i in range(min(4, len(lineas))):
                            self.stdscr.addstr(inicio_y_descripcion + i, inicio_x_izquierda + 2, lineas[i])
    
                if mostrar_ayuda:
                    self.mostrar_ayuda()
    
                if max_y > 1:
                    self.stdscr.addstr(max_y - 1, 0, MENSAJE_AYUDA)
    
                self.stdscr.refresh()
    
                try:
                    tecla = self.stdscr.getch()  
                except KeyboardInterrupt:
                    break  
    
                if tecla == TECLA_SALIR:
                    if self.confirmar_salida():
                        break
                elif tecla == TECLA_AYUDA:
                    mostrar_ayuda = not mostrar_ayuda  
                    if mostrar_ayuda:
                        self.mostrar_ayuda()
                        mostrar_ayuda = False
                        continue
                elif tecla == TECLA_DESHACER:
                    self.deshacer_cambio()
                elif tecla in [curses.KEY_ENTER, 10] and (self.columna_actual == 1):
                    if (self.seleccion_actual_derecha < len(subapartados)):
                        subapartado_seleccionado = subapartados[self.seleccion_actual_derecha]
                        nuevo_valor = self.entrada_emergente(f"Ingrese nuevo valor para {subapartado_seleccionado.nombre}:")
                        subapartado_seleccionado.valor = nuevo_valor
                        if subapartado_seleccionado.linea:
                            self.personalizacion.actualizar_archivo(apartado_seleccionado.ruta,
                                                             subapartado_seleccionado.linea.rstrip('*'), nuevo_valor)
                            self.mostrar_mensaje("Valor actualizado correctamente")
                else:
                    cantidad_opciones_izquierda = len(opciones_izquierda)
                    cantidad_opciones_derecha = len(opciones_derecha)
                    
                    self.manejar_navegacion(tecla, cantidad_opciones_izquierda, cantidad_opciones_derecha)
    
        except Exception as e:
            print(f"Error en bucle_principal: {e}")

    def confirmar_salida(self) -> bool:
        try:
            return self.entrada_emergente("¿Estás seguro de que quieres salir? (s/n)").lower() == 's'
        except Exception as e:
            print(f"Error en confirmar_salida: {e}")
            return False

    def mostrar_mensaje(self, mensaje: str) -> None:
        try:
            max_y, max_x = self.stdscr.getmaxyx()
            altura, ancho = 3, len(mensaje) + 10
            inicio_y, inicio_x = (max_y - altura) // 2, (max_x - ancho) // 2

            self.dibujar_ventana_bordeada(inicio_y, inicio_x, altura, ancho, TITULO_MENSAJE)
            self.stdscr.addstr(inicio_y + 1, inicio_x + 5, mensaje)
            self.stdscr.refresh()
            
            time.sleep(TIEMPO_MENSAJE)

            self.stdscr.clear()
        except Exception as e:
            print(f"Error al mostrar mensaje: {e}")

    def manejar_navegacion(self, tecla: int, cantidad_opciones_izquierda: int, cantidad_opciones_derecha: int):
        try:
            if tecla == curses.KEY_UP:
                if self.columna_actual == 0 and self.seleccion_actual_izquierda > 0:
                    self.seleccion_actual_izquierda -= 1
                elif self.columna_actual == 1 and self.seleccion_actual_derecha > 0:
                    self.seleccion_actual_derecha -= 1
            elif tecla == curses.KEY_DOWN:
                if self.columna_actual == 0 and self.seleccion_actual_izquierda < cantidad_opciones_izquierda - 1:
                    self.seleccion_actual_izquierda += 1
                elif self.columna_actual == 1 and self.seleccion_actual_derecha < cantidad_opciones_derecha - 1:
                    self.seleccion_actual_derecha += 1
            elif tecla == curses.KEY_LEFT and self.columna_actual > 0:
                self.columna_actual -= 1
            elif tecla == curses.KEY_RIGHT and self.columna_actual < 1:
                self.columna_actual += 1
        except Exception as e:
            print(f"Error en manejar_navegacion: {e}")

    def deshacer_cambio(self):
        cambio = self.personalizacion.deshacer_ultimo_cambio()
        if cambio:
            self.mostrar_mensaje(f"Deshecho: {cambio}")
        else:
            self.mostrar_mensaje("No hay cambios para deshacer")
