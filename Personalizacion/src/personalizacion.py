import os
import fileinput
from typing import List, Optional, Dict


class Apartado:
    def __init__(self, nombre: str, ruta: str, identidad: int):
        self.nombre = nombre
        self.ruta = ruta
        self.identidad = identidad


class Subapartado:
    def __init__(self, apartado: int, nombre: str, linea: Optional[str], valor: Optional[str], identidad: int, descripcion: str):
        self.apartado = apartado
        self.nombre = nombre
        self.linea = linea
        self.valor = valor
        self.identidad = identidad
        self.descripcion = descripcion


class Personalizacion:
    def __init__(self):
        try:
            #apartados principales
            self.apartados: List[Apartado] = [
                Apartado("Terminal", os.path.expanduser("~/.config/kitty/kitty.conf"), 1),
                Apartado("Gestor De Ventanas", os.path.expanduser("~/.config/qtile/config.py"), 2)
            ]

            #subapartados
            self.subapartados: List[Subapartado] = [
                #los subapartados para Kitty.conf
                Subapartado(1, "Color De Fondo", "background*", "*#0abdc6", 100,
                            "Cambia el color de fondo de la terminal. Usa códigos hexadecimales."),
                Subapartado(1, "Color De Letra", "foreground*", "*#ffffff", 101,
                            "Modifica el color del texto en la terminal. Usa códigos hexadecimales."),
                Subapartado(1, "Fuente", "font_family", "Ubuntu Mono", 102,
                            "Cambia la fuente principal de la terminal. Asegúrate de que la fuente esté instalada en tu sistema."),
                Subapartado(1, "Dimensiones de Fuente", "font_size", "11.0", 103,
                            "Ajusta las dimensiones de la fuente. Usa valores numéricos, por ejemplo: 11.0"),
                Subapartado(1, "Color de Ventana Activa", "active_tab_background", "#eee", 104,
                            "Cambia el color de fondo de la ventana activa. Usa códigos hexadecimales."),
                Subapartado(1, "Color de Ventana Inactiva", "inactive_tab_background", "#999", 105,
                            "Cambia el color de fondo de las ventanas inactivas. Usa códigos hexadecimales."),
                Subapartado(1, "Estilo de Ventana", "tab_bar_style", "powerline", 106,
                            "Cambia el estilo de la barra de ventana. Opciones: fade, slant, separator, powerline, custom."),
                Subapartado(1, "Color de Cursor", "cursor", "#cccccc", 107,
                            "Cambia el color del cursor. Usa códigos hexadecimales."),
                Subapartado(1, "Color de Selección", "selection_background", "#555555", 108,
                            "Cambia el color del texto seleccionado. Usa códigos hexadecimales."),

                #los subapartados para Qtile
                Subapartado(2, "Barra De Estado", "bar = bar", "bar = bar", 202,
                            "Personaliza la barra superior de Qtile. Puedes modificar colores, agregar widgets o cambiar fuentes."),
                Subapartado(2, "Atajos De Teclado", "keys = [", "keys = [", 203,
                            "Define combinaciones de teclas para acciones rápidas como cambiar espacios de trabajo o abrir aplicaciones."),
                Subapartado(2, "Layouts", "layouts = [", "layouts = [", 204,
                            "Configura cómo se organizan las ventanas. Opciones: Mosaico, Columnas, Flotante, Máximo, Matriz."),
                Subapartado(2, "Grupos", "groups = [", "groups = [", 205,
                            "Crea escritorios virtuales y asigna nombres o aplicaciones predeterminadas."),
                Subapartado(2, "Widgets", "widget.", "widget.", 206,
                            "Agrega información en la barra como reloj o estadísticas del sistema."),
                Subapartado(2, "Múltiples Monitores", "screens = [", "screens = [", 207,
                            "Configura el comportamiento en pantallas múltiples y distribuye espacios de trabajo."),
                Subapartado(2, "Autostart", "autostart = [", "[autostart]", 208,
                            "Define programas que se inician automáticamente con Qtile."),
                Subapartado(2, "Reglas De Ventanas", "floating_layout = layout.Floating(", "floating_layout = layout.Floating(", 209, 
                            "Establece comportamientos especificos para ciertas aplicaciones, como ventanas flotantes."),
                Subapartado(2, "Hooks", "@hook.subscribe.", "@hook.subscribe.", 210, 
                            "Configura acciones automaticas en eventos del sistema, como al iniciar sesion o abrir/cerrar ventanas."),
                Subapartado(2, "Configuracion De Mouse", "mouse = [", "mouse = [", 211, 
                            "Define acciones para los botones del raton en diferentes contextos de la interfaz."),
            ]
            #creo un diccionario para almacenar subapartados por apartado
            self._subapartados_por_apartado: Dict[int, List[Subapartado]] = {}
            self.cambios: List[str] = []
        except Exception as e:
            print(f"Error al inicializar Personalizacion: {e}")
            raise

    def obtener_subapartados_para_apartado(self, identidad_apartado: int) -> List[Subapartado]:
        """
        Devuelve los subapartados asociados a un apartado dado.
        """
        try:
            if identidad_apartado not in self._subapartados_por_apartado:
                self._subapartados_por_apartado[identidad_apartado] = [
                    s for s in self.subapartados if s.apartado == identidad_apartado
                ]
            return self._subapartados_por_apartado[identidad_apartado]
        except Exception as e:
            print(f"Error al obtener subapartados: {e}")
            return []

    def actualizar_archivo(self, ruta_apartado: str, prefijo_linea: str, nuevo_valor: str) -> None:
        """
        Actualiza una línea específica en un archivo con un nuevo valor.
        """
        nueva_linea = f"{prefijo_linea} {nuevo_valor}"
        try:
            with fileinput.input(ruta_apartado, inplace=True) as archivo:
                for linea in archivo:
                    print(nueva_linea if linea.startswith(prefijo_linea) else linea.rstrip(), end='\n')
            self.cambios.append(f"Actualizado: {prefijo_linea} a {nuevo_valor}")
        except IOError as e:
            print(f"Error al actualizar el archivo: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar el archivo: {e}")

    def deshacer_ultimo_cambio(self) -> Optional[str]:
        """
        Deshace el último cambio realizado en un archivo.
        """
        if self.cambios:
            return self.cambios.pop()
        return None
