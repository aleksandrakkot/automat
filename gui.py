import tkinter as tk
from functools import partial


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        monety_frame = tk.Frame(master=self) #tworzymy sobie ramke przechowujaca przyciski a jego rodzicem (ramka nadrzedna) jest to okno czyli self
        nominaly = ["5zł", "2zł", "1zł", "50gr", "20gr", "10gr", "5gr", "2gr", "1gr"]
        for nominal in nominaly:
            b = tk.Button(master=monety_frame, text=nominal, width=10, height=5)
            b.pack() #zapakuj sie do ramki

        #pakujemy ramke do okna
        monety_frame.grid(column=0, row=0)

        prawy_frame = tk.Frame(master=self)

        info_frame = tk.Frame(master=prawy_frame)
        L1 = tk.Label(master=info_frame, text="Nr towaru")
        L1.pack(side=tk.LEFT)

        self.cyfry_var = tk.StringVar()
        E1 = tk.Entry(master=info_frame, bd=5, textvariable=self.cyfry_var)
        E1.pack(side=tk.RIGHT)
        info_frame.grid(column=0, row=0)

        cyfry_frame = tk.Frame(master=prawy_frame)
        cyfry = [["1", "2", "3"],
                 ["4", "5", "6"],
                 ["7", "8", "9"],
                 ["C", "0", "R"]]

        for i in range(len(cyfry)):
            for j in range(len(cyfry[i])):
                b = tk.Button(master=cyfry_frame,
                              text=cyfry[i][j],
                              width=10,
                              height=5,
                              command=partial(self.przycisk_cyfra_akcja, cyfry[i][j])) #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
                b.grid(row=i, column=j)

        cyfry_frame.grid(column=0, row=1)
        prawy_frame.grid(column=1, row=0)

    def przycisk_cyfra_akcja(self, nr):
        if nr.isdigit():
            text = self.cyfry_var.get() + nr
            self.cyfry_var.set(text)
        elif nr == "C":
            self.cyfry_var.set("")
        #TODO: dodac realizacje zamowienia (R)


    def start(self):
        self.mainloop()