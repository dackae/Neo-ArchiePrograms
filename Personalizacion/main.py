import curses
from src import Personalizacion, InterfazUsuario

def main(stdscr):
    from src import Personalizacion, InterfazUsuario
    try:
        #iniciamos la personalización
        personalizacion = Personalizacion()
        
        #creamos la interfaz de usuario
        ui = InterfazUsuario(stdscr, personalizacion)
        
        #iniciamos el bucle principal
        ui.bucle_principal()
    except Exception as e:
        print(f"Error en main: {e}")

if __name__ == "__main__":
    try:
        #tenemos que usar el wrapper de curses iniciarlo
        curses.wrapper(main)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
