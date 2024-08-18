import colors

class Colorizer(colors.Bcolors):
    def __init__(self, color):
        self.color = self.COLORS.get(color, self.COLORS['reset'])

    def __enter__(self):
        print(self.color, end='')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(self.COLORS['reset'], end='')


print('\033[93m', end='')
print('aaa')
print('bbb')
print('\033[0m', end='')
print('ccc')

with Colorizer('red'):
    print('printed in red')
print('printed in default color')