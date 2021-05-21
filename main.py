import random


class Towar:
    def __init__(self, nr, cena, ilosc=5):
        self.nr = nr
        self.cena = cena
        self.ilosc = ilosc #TODO: zrobi getery i setery dekoratorami

    def __str__(self):
        return f"Nr: {self.nr} Cena: {self.cena} Ilosc: {self.ilosc}"


towary = [Towar(i, round(random.randrange(1, 5) + random.randrange(0, 100)/100, 2)) for i in range(30, 51)]
for towar in towary:
    print(towar)


class Automat:
    def __init__(self, towary):
        self.towary = towary
        self.monety_wrzucone = []
        self.monety_reszta = []

    def wrzuc(self, moneta):
        self.monety_wrzucone.append(moneta)

    def pobierz_towar(self, nr):
        try:
            return [towar for towar in self.towary if towar.nr == nr][0]
        except IndexError:
            return None

    def podaj_reszte(self, ile_reszty):
        reszta_do_wydania = []
        monetki = self.monety_reszta + self.monety_wrzucone
        monetki.sort(reverse=True)
        index = 0
        while ile_reszty > 0 and index < len(monetki):
            if monetki[index] <= ile_reszty:
                ile_reszty -= monetki[index]
                reszta_do_wydania.append(monetki[index])
            index += 1
        if ile_reszty == 0:
            return reszta_do_wydania

    def zamowienie(self, nr):
        towar = self.pobierz_towar(nr)

        if not towar:
            return "brak towaru o danym numerze"

        reszta = sum(self.monety_wrzucone) - towar.cena
        if reszta < 0:
            return "niewystarczajace srodki"

        if towar.ilosc == 0:
            return "brak towaru na stanie"

        reszta_do_wydania = self.monety_reszta(reszta)
        if reszta_do_wydania != 0:
            towar.ilosc -= 1
            self.monety_reszta.extend(self.monety_wrzucone)
            self.monety_wrzucone.clear()
            for moneta in reszta_do_wydania:
                self.monety_reszta.remove(moneta)
            return f"Kupilas towar, wydano: {reszta_do_wydania}"
        else:
            return "nie mozna wydac reszty"


