import os

class MaskFunc:
    def getch():
        # if windows system
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8')
        # if unix based system
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    # masks password while asking for input with asterisks
    def get_masked_password(self):
        # TODO: if else statement with second part for unix based
        password = ''
        while True:
            ch = self.getch()
            # if enter is pressed, break
            if ch == '\n' or ch == '\r':
                break
            # if backspace is pressed
            elif ch == '\x08' or ch == '\x7f':
                if len(password) > 0:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            # if pressed char is printable, add asterisks, else dont
            elif 32 <= ord(ch) <= 126:
                password += ch
                print('*', end='', flush=True)
        print()
        return str(password)