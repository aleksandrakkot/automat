import random


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


class Automat:
    def __init__(self, towary):
        self.__towary = towary
        self.__monety_wrzucone = []
        self.__monety_reszta = []

    def wrzuc(self, moneta):
        self.__monety_wrzucone.append(moneta)

    def pobierz_towar(self, nr):
        try:
            return [towar for towar in self.__towary if towar.nr == nr][0]
        except IndexError:
            return None

    def anuluj(self):
        self.__monety_wrzucone.clear()

    def podaj_reszte(self, ile_reszty):
        reszta_do_wydania = []
        monetki = self.__monety_reszta + self.__monety_wrzucone
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

        reszta = sum(self.__monety_wrzucone) - towar.cena
        if reszta < 0:
            return "niewystarczajace srodki"

        if towar.ilosc == 0:
            return "brak towaru na stanie"

        reszta_do_wydania = self.__monety_reszta(reszta)
        if reszta_do_wydania != 0:
            towar.ilosc -= 1
            self.__monety_reszta.extend(self.__monety_wrzucone)
            self.__monety_wrzucone.clear()
            for moneta in reszta_do_wydania:
                self.__monety_reszta.remove(moneta)
            return f"Kupilas towar, wydano: {reszta_do_wydania}"
        else:
            return "nie mozna wydac reszty"


