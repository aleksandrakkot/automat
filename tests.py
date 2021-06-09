import unittest
from maszyna import Automat, Towar


class Testy(unittest.TestCase):
    def setUp(self):
        self.automat = Automat([Towar(cena=3.5, nr=15, ilosc=5)])

    def test_sprawdz_cene(self): #sprawdzenie ceny jednego towaru
        towar = self.automat.pobierz_towar(15)
        self.assertIsNotNone(towar, "Brak towaru")
        self.assertEqual(towar.cena, 3.5, "Niepoprawna cena")

    def test_kupno_po_odliczonej_kwocie(self): #wrzucenie odliczonej kwoty,zakup towaru - brak reszty
        self.automat.wrzuc(3)
        self.automat.wrzuc(0.5)
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertTrue(status)
        self.assertEqual(reszta, 0)

    def test_kupno_po_wiekszej_kwocie(self): #wrzucenie odliczonej kwoty,zakup towaru - reszta
        self.automat.wrzuc(3)
        self.automat.wrzuc(0.5)
        self.automat.wrzuc(0.5)
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertTrue(status)
        self.assertEqual(reszta, 0.5)

    def test_kupno_do_wyczerpania_zapasow(self): #wykupienie całego asortymentu
        for i in range(5):
            self.automat.wrzuc(3)
            self.automat.wrzuc(0.5)
            self.automat.zamowienie(15)
        self.automat.wrzuc(3)
        self.automat.wrzuc(0.5)
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertEqual(msg, "brak towaru na stanie")
        self.assertFalse(status)

    def test_sprawdzenie_towaru_o_niepoprawnym_nr(self): #sprawdzenie towaru i nieprawidłowym numerze
        self.assertIsNone(self.automat.pobierz_towar(555))

    def test_wrzuc_monety_i_anuluj(self): #przerwanie transakcji
        monety = [1, 5, 0.5, 2]
        [self.automat.wrzuc(x) for x in monety]
        self.assertEqual(self.automat.anuluj(), monety)

    def test_zamowienie_z_doplata(self): #wrzucenie za małek kwoty i dopłata
        self.automat.wrzuc(2)
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertFalse(status)
        self.assertEqual(msg, "niewystarczajace srodki")
        self.automat.wrzuc(1)
        self.automat.wrzuc(0.5)
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertTrue(status)
        self.assertEqual(reszta, 0)

    def test_wplacanie_po_groszu(self): #zakup toawru płacąc po 1 gr
        [self.automat.wrzuc(0.01) for i in range(350)]
        msg, status, reszta = self.automat.zamowienie(15)
        self.assertTrue(status)
        self.assertEqual(reszta, 0)

if __name__ == '__main__':
    unittest.main()