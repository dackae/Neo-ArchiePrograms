class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def display(self, options):
        self.stdscr.clear()
        for i, option in enumerate(options):
            self.stdscr.addstr(i+1, 2, f"{i+1}. {option}")
        self.stdscr.refresh()

    def get_selection(self, options):
        self.display(options)
        while True:
            key = self.stdscr.getch()
            if ord('1') <= key <= ord(str(len(options))):
                return int(chr(key)) - 1