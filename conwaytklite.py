from random import randint
from tkinter import Button, Frame, Label, Menu, Tk


class ConwayTk:
    def __init__(self, columns=40, rows=32, interval=120, cell_size=1, random=False):
        self.rows = rows
        self.columns = columns
        self.interval = interval
        self.cell_size = cell_size
        self.data_array = self.create_2d_array(random=random)
        self.button_array = self.create_2d_array(value=None)
        self.paused = True


    def create_2d_array(self, value=0, random=False):
        return [[value if not random else randint(0, 1) for _ in range(self.rows)] for _ in range(self.columns)]


    def draw_grid(self):
        loading = Label(self.root, font=('Calibri', 36), text='Loading...')
        loading.place(relx=0.4, rely=0.4)
        
        for x in range(self.rows):
            for y in range(self.columns):
                if self.data_array[y][x] == 0:
                    button = Button(self.grid_frame, bg='black')
                else:
                    button = Button(self.grid_frame, bg='white')
                button.config(height=self.cell_size, width=self.cell_size*2, bd=1, relief='solid', command=lambda x=x, y=y, b=button: self.click(x, y, b))
                button.grid(row=x, column=y)
                self.button_array[y][x] = button
        
        loading.after(100, loading.destroy)

    
    def get_neighbors(self, x, y):
        total = 0

        for m in range(-1, 2):
            for n in range(-1, 2):
                x_ = (x+m+self.rows) % self.rows
                y_ = (y+n+self.columns) % self.columns
                total += self.data_array[y_][x_]
                
        return total-self.data_array[y][x]
    

    def click(self, x, y, button):
        if button['bg'] == 'black':
            self.data_array[y][x] = 1
            button['bg'] = 'white'
        else:
            self.data_array[y][x] = 0
            button['bg'] = 'black'


    def pause(self):
        self.paused = not self.paused
        self.life(self.paused)


    def reset(self):
        self.root.destroy()
        self.paused = True
        self.data_array = self.create_2d_array(random=True)
        self.run()
    

    def clear(self):
        self.root.destroy()
        self.paused = True
        self.data_array = self.create_2d_array(value=0)
        self.run()


    def life(self, paused):
        next_cycle = self.create_2d_array(value=0)

        if not paused:
            while True:
                for x in range(self.rows):
                    for y in range(self.columns):
                        state = self.data_array[y][x]
                        neighbors = self.get_neighbors(x, y)
                        if state == 0 and neighbors == 3:
                            self.button_array[y][x].config(bg='white')
                            next_cycle[y][x] = 1
                        elif state == 1 and (neighbors < 2 or neighbors > 3):
                            self.button_array[y][x].config(bg='black')
                            next_cycle[y][x] = 0
                        else:
                            next_cycle[y][x] = state
                self.data_array = next_cycle
                self.root.after(self.interval, lambda: self.life(self.paused))
                if self.root.destroy:
                    return False


    def run(self):
        self.root = Tk()
        self.root.title('Conway\'s Game of Life (Lite Version)')
        self.root.resizable(0, 0)
        
        self.bg_frame = Frame(self.root)
        self.grid_frame = Frame(self.bg_frame)

        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Pause', command=self.pause, accelerator='|   Space')
        self.file_menu.add_command(label='Reset', command=self.reset, accelerator='|   Ctrl+R')
        self.file_menu.add_command(label='Clear', command=self.clear, accelerator='|   Ctrl+C')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.destroy, accelerator='|   Alt+F4')

        self.bg_frame.pack(expand=True, fill='both')
        self.grid_frame.pack(side='top', anchor='c')

        self.draw_grid()
        self.life(self.paused)

        self.root.bind_all('<space>', lambda _: self.pause())
        self.root.bind_all('<Control-r>', lambda _: self.reset())
        self.root.bind_all('<Control-R>', lambda _: self.reset())
        self.root.bind_all('<Control-c>', lambda _: self.clear())
        self.root.bind_all('<Control-C>', lambda _: self.clear())

        self.root.config(menu=self.menu_bar)
        self.root.focus_force()
        self.root.mainloop()


if __name__ == '__main__':
    game = ConwayTk(random=True)
    game.run()
