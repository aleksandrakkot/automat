import tkinter as tk
import tkinter.messagebox as msg
from functools import partial
from maszyna import Automat, nominaly, Towar


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.title("Automat")
        self.automat = Automat(towary=Towar.stworz_towary())

    def init_window(self):
        monety_frame = tk.Frame(master=self) #tworzymy sobie ramke przechowujaca przyciski a jego rodzicem (ramka nadrzedna) jest to okno czyli self
        for nominal in nominaly:
            b = tk.Button(master=monety_frame, text=nominal, width=10, height=5, command=partial(self.przycisk_wplata_akcja, nominal))
            b.pack() #zapakuj sie do ramki

        #pakujemy ramke do okna
        monety_frame.grid(column=0, row=0)

        prawy_frame = tk.Frame(master=self)

        info_frame, self.cyfry_var = self.create_numeric_info(prawy_frame, "Nr towaru")
        info_frame.grid(column=0, row=0)

        info_frame2, self.wplata = self.create_numeric_info(prawy_frame, "Wpłata")
        info_frame2.grid(column=0, row=1)

        info_frame3, self.cena_towaru = self.create_numeric_info(prawy_frame, "Cena")
        info_frame3.grid(column=0, row=2)

        cyfry_frame = tk.Frame(master=prawy_frame)
        cyfry = [["1", "2", "3"],
                 ["4", "5", "6"],
                 ["7", "8", "9"],
                 ["@", "0", "R"]]

        for i in range(len(cyfry)):
            for j in range(len(cyfry[i])):
                b = tk.Button(master=cyfry_frame,
                              text=cyfry[i][j],
                              width=10,
                              height=5,
                              command=partial(self.przycisk_cyfra_akcja, cyfry[i][j])) #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
                b.grid(row=i, column=j)

        cyfry_frame.grid(column=0, row=3)
        prawy_frame.grid(column=1, row=0)

    def przycisk_cyfra_akcja(self, nr):
        if nr.isdigit():
            text = self.cyfry_var.get() + nr
            self.cyfry_var.set(text)
            towar = self.automat.pobierz_towar(int(text))
            self.cena_towaru.set(str(towar.cena) + "zł" if towar else "")
        elif nr == "R":
            self.cyfry_var.set("")
            self.cena_towaru.set("")
            self.wplata.set("")
            self.automat.anuluj()
        elif nr == "@":
            if self.cyfry_var.get() == "":
                msg.showinfo("Błąd", "Nie podano nr towaru!")
            else:
                wiadomosc, ok, reszta = self.automat.zamowienie(int(self.cyfry_var.get()))
                if ok:
                    msg.showinfo("Wykonano!", wiadomosc)
                    self.cyfry_var.set("")
                    self.wplata.set("")
                else:
                    msg.showerror("Błąd", wiadomosc)



    def przycisk_wplata_akcja(self, moneta_str):
        moneta = nominaly[moneta_str]
        self.automat.wrzuc(moneta)
        self.wplata.set(f"{self.automat.suma_wplat()}zł")

    def create_numeric_info(self, master, text):
        info_frame = tk.Frame(master=master)
        L1 = tk.Label(master=info_frame, text=text)
        L1.pack(side=tk.LEFT)

        var = tk.StringVar()
        E1 = tk.Entry(master=info_frame, bd=5, textvariable=var, state=tk.DISABLED)
        E1.pack(side=tk.RIGHT)
        return info_frame, var

    def start(self):
        self.mainloop()