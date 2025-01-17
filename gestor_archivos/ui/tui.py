import curses
import os
import subprocess
from funciones_ficheros import listar_archivos, copiar_archivo, mover_archivo, eliminar_archivo, crear_directorio
from utils.utilidades_archivos import obtener_info_archivo
from ui.menu import Menu

class FileManagerTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.height, self.width = stdscr.getmaxyx()
        self.current_dir = os.path.expanduser("~")
        self.files = []
        self.selected_index = 0
        self.menu = Menu(stdscr)

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Directorio actual: {self.current_dir}")
        self.files = ['..' if i == 0 else f for i, f in enumerate(['..'] + listar_archivos(self.current_dir))]
        max_display = min(len(self.files), self.height - 3)
        for i in range(max_display):
            if i == self.selected_index:
                self.stdscr.addstr(i+2, 0, f"> {self.files[i]}"[:self.width-1], curses.A_REVERSE)
            else:
                self.stdscr.addstr(i+2, 0, f"  {self.files[i]}"[:self.width-1])
        self.stdscr.addstr(self.height-1, 0, "q: Salir | m: Menú | Backspace: Directorio anterior")
        self.stdscr.refresh()

    def run(self):
        while True:
            self.display()
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif key == curses.KEY_DOWN:
                self.selected_index = min(len(self.files) - 1, self.selected_index + 1)
            elif key == ord('\n'):  # Enter
                self.enter_directory()
            elif key == ord('m'):
                self.show_menu()
            elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
                self.go_to_parent_directory()

    def enter_directory(self):
        selected_file = self.files[self.selected_index]
        if selected_file == '..':
            self.go_to_parent_directory()
        else:
            path = os.path.join(self.current_dir, selected_file)
            if os.path.isdir(path):
                self.current_dir = path
                self.selected_index = 0
            elif os.path.isfile(path):
                self.show_file_info()

    def go_to_parent_directory(self):
        parent_dir = os.path.dirname(self.current_dir)
        if parent_dir != self.current_dir:
            self.current_dir = parent_dir
            self.selected_index = 0

    def show_menu(self):
        options = ["Copiar", "Mover", "Eliminar", "Crear archivo/directorio", "Info", "Cancelar"]
        selection = self.menu.get_selection(options)
        if selection == 0:
            self.copy_file()
        elif selection == 1:
            self.move_file()
        elif selection == 2:
            self.delete_file()
        elif selection == 3:
            self.create_file_or_directory()
        elif selection == 4:
            self.show_file_info()
        elif selection == 5:
            pass

    def copy_file(self):
        source = os.path.join(self.current_dir, self.files[self.selected_index])
        destination = self.get_user_input("Ingrese la ruta de destino: ")
        try:
            copiar_archivo(source, destination)
            self.show_message("Archivo copiado exitosamente.")
        except Exception as e:
            self.show_message(f"Error al copiar: {str(e)}")

    def move_file(self):
        source = os.path.join(self.current_dir, self.files[self.selected_index])
        destination = self.get_user_input("Ingrese la ruta de destino: ")
        try:
            mover_archivo(source, destination)
            self.show_message("Archivo movido exitosamente.")
        except Exception as e:
            self.show_message(f"Error al mover: {str(e)}")

    def delete_file(self):
        file_to_delete = os.path.join(self.current_dir, self.files[self.selected_index])
        confirm = self.get_user_input(f"¿Está seguro de eliminar {self.files[self.selected_index]}? (s/n): ")
        if confirm.lower() == 's':
            try:
                eliminar_archivo(file_to_delete)
                self.show_message("Archivo eliminado exitosamente.")
            except Exception as e:
                self.show_message(f"Error al eliminar: {str(e)}")

    def create_file_or_directory(self):
        name = self.get_user_input("Ingrese el nombre del nuevo archivo/directorio: ")
        path = os.path.join(self.current_dir, name)
        if name.endswith('/'):
            try:
                crear_directorio(path)
                self.show_message("Directorio creado exitosamente.")
            except Exception as e:
                self.show_message(f"Error al crear directorio: {str(e)}")
        else:
            try:
                with open(path, 'w') as f:
                    pass
                subprocess.run(['nano', path])
                self.show_message("Archivo creado y editado exitosamente.")
            except Exception as e:
                self.show_message(f"Error al crear/editar archivo: {str(e)}")

    def show_file_info(self):
        file_path = os.path.join(self.current_dir, self.files[self.selected_index])
        info = obtener_info_archivo(file_path)
        info_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
        self.show_message(info_str, title="Información del archivo")

    def get_user_input(self, prompt):
        curses.echo()
        self.stdscr.addstr(self.height-1, 0, prompt)
        self.stdscr.refresh()
        input_str = self.stdscr.getstr(self.height-1, len(prompt)).decode('utf-8')
        curses.noecho()
        return input_str

    def show_message(self, message, title="Mensaje"):
        message_lines = message.split('\n')
        max_width = max(len(line) for line in message_lines)
        height = len(message_lines) + 4
        width = max_width + 4
        y = (self.height - height) // 2
        x = (self.width - width) // 2
        
        message_win = curses.newwin(height, width, y, x)
        message_win.box()
        message_win.addstr(1, 2, title, curses.A_BOLD)
        for i, line in enumerate(message_lines):
            message_win.addstr(i+2, 2, line)
        message_win.addstr(height-2, 2, "Presione cualquier tecla para continuar...")
        message_win.refresh()
        message_win.getch()
