import curses

#para los colores
COLOR_FONDO = curses.COLOR_CYAN
COLOR_TEXTO = curses.COLOR_BLACK

#para el tamaño
ALTURA_MINIMA = 20
ANCHO_MINIMO = 80

#para los mensajes
MENSAJE_PANTALLA_PEQUENA = "Usa una pantalla más grande para usar el programa"
MENSAJE_AYUDA = "Presiona 'h' para ayuda, 'q' para salir, 'u' para deshacer"

#para las teclas
TECLA_SALIR = ord('q')
TECLA_AYUDA = ord('h')
TECLA_DESHACER = ord('u')

#para los titulos de ventanas
TITULO_COLUMNA_IZQUIERDA = "Columna Izquierda"
TITULO_COLUMNA_DERECHA = "Columna Derecha"
TITULO_ENTRADA = "Entrada"
TITULO_MENSAJE = "Mensaje"
TITULO_AYUDA = "Ayuda"

#para los textos de ayuda
TEXTO_AYUDA = [
    "Teclas de navegación:",
    "- Arriba/abajo: Navegar opciones",
    "- Izquierda/derecha: Cambiar columnas",
    "- Enter: Seleccionar opción",
    "- q: Salir",
    "- h: Mostrar/ocultar ayuda",
    "- u: Deshacer último cambio"
]

#para los tiempos del popup (va en segundos)
TIEMPO_MENSAJE = 2
