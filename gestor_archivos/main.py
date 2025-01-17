import curses
import locale
from ui.tui import FileManagerTUI

def main(stdscr):
    #Configurar la localización para manejar caracteres Unicode
    locale.setlocale(locale.LC_ALL, '')

    #Configurar curses para manejar caracteres Unicode
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    try:
        #verificar el tamaño mínimo de la terminal
        height, width = stdscr.getmaxyx()
        if height < 10 or width < 40:
            raise curses.error("Terminal es muy pequeña!")

        fm = FileManagerTUI(stdscr)
        fm.run()
    except curses.error as e:
        #Salir de curses temporalmente para mostrar el error
        curses.endwin()
        print(f"Se produjo un error de curses: {e}")
        print("Asegúrate de que tu terminal sea lo suficientemente grande y soporte caracteres Unicode.")
    except Exception as e:
        #Manejar cualquier otra excepción
        curses.endwin()
        print(f"Se produjo un error inesperado: {e}")

if __name__ == "__main__":
    curses.wrapper(main)
