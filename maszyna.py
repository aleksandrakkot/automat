import random

nominaly = {"5zł" : 5,
             "2zł" : 2,
             "1zł" : 1,
             "50gr" : 0.5,
             "20gr" : 0.2,
             "10gr" : 0.1,
             "5gr" : 0.05,
             "2gr" : 0.02,
             "1gr": 0.01
             }


class Towar:
    @staticmethod
    def stworz_towary():
        return [Towar(i, round(random.randrange(1, 5) + random.randrange(0, 100) / 100, 2)) for i in range(30, 51)]

    def __init__(self, nr, cena, ilosc=5):
        self.__nr = nr
        self.__cena = cena
        self.__ilosc = ilosc

    def __str__(self):
        return f"Nr: {self.__nr} Cena: {self.__cena} Ilosc: {self.__ilosc}"

    @property #getter tylko ze nie trzeba dawac juz nawiasow (np towar.nr()) dzieki dekoratorowi @property
    def nr(self):
        return self.__nr

    @property
    def cena(self):
        return self.__cena

    @property
    def ilosc(self):
        return self.__ilosc

    @ilosc.setter
    def ilosc(self, value):
        self.__ilosc = value

class Automat:
    def __init__(self, towary):
        for towar in towary:
            print(towar)
        self.__towary = towary
        self.__monety_wrzucone = []
        self.__monety_reszta = []

    def wrzuc(self, moneta):
        self.__monety_wrzucone.append(moneta)

    def suma_wplat(self):
        return round(sum(self.__monety_wrzucone), 2)

    def pobierz_towar(self, nr):
        try:
            return [towar for towar in self.__towary if towar.nr == nr][0]
        except IndexError:
            return None

    def anuluj(self):
        monety = self.__monety_wrzucone.copy()
        self.__monety_wrzucone.clear()
        return monety

    def podaj_reszte(self, ile_reszty):
        ile_reszty = round(ile_reszty, 2)
        reszta_do_wydania = []
        monetki = self.__monety_reszta + self.__monety_wrzucone
        monetki.sort(reverse=True)
        index = 0
        while ile_reszty > 0 and index < len(monetki):
            if monetki[index] <= ile_reszty:
                ile_reszty -= monetki[index]
                ile_reszty = round(ile_reszty, 2)
                reszta_do_wydania.append(monetki[index])
            index += 1
        if ile_reszty == 0:
            return reszta_do_wydania

    def zamowienie(self, nr):
        sukces = False
        towar = self.pobierz_towar(nr)

        if not towar:
            return "brak towaru o danym numerze", sukces, 0
        x = sum(self.__monety_wrzucone)
        reszta = round(sum(self.__monety_wrzucone), 2) - towar.cena
        if reszta < 0:
            return "niewystarczajace srodki", sukces, 0

        if towar.ilosc == 0:
            return "brak towaru na stanie", sukces, 0

        reszta_do_wydania = self.podaj_reszte(reszta)
        if reszta_do_wydania is not None:
            towar.ilosc -= 1
            self.__monety_reszta.extend(self.__monety_wrzucone)
            self.__monety_wrzucone.clear()
            for moneta in reszta_do_wydania:
                self.__monety_reszta.remove(moneta)
            sukces = True
            return f"Kupilas towar, wydano reszty: {sum(reszta_do_wydania)}zł", sukces, sum(reszta_do_wydania)
        else:
            return "nie mozna wydac reszty", sukces, 0


