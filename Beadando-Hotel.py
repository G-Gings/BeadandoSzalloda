from datetime import datetime
from abc import ABC, abstractmethod

class Szoba(ABC):
    @abstractmethod
    def __init__(self, szobsz, ar):
        self.szobsz = szobsz
        self.ar = ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobsz, bath):
        super().__init__(szobsz, 40000)
        self.bath = bath


class KetagyasSzoba(Szoba):
    def __init__(self, szobsz, extra):
        super().__init__(szobsz, 90000)
        self.extra = extra


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.fogl_ok = []


    def plus_szoba(self, szoba):
        self.szobak.append(szoba)


    def fogl(self, szobsz, datum):
        for fogl in self.fogl_ok:
            if fogl.szoba.szobsz == szobsz and fogl.datum == datum:
                print("\nA választott szobát már lefoglalták ezen a napon. \nKérjük válasszon másik szobát vagy másik dátumot!")
                return
        for szoba in self.szobak:
            if szoba.szobsz == szobsz:
                self.fogl_ok.append(Foglalas(szoba, datum))
                print("Sikeres foglalás!")
                return szoba.ar
        print("\nA megadott szobaszám nem létezik a szállodában.")

    def lemond(self, szobsz, datum):
        for fogl in self.fogl_ok:
            if fogl.szoba.szobsz == szobsz and fogl.datum == datum:
                self.fogl_ok.remove(fogl)
                return True
        return False

    def list_fogl_ok(self):
        for fogl in self.fogl_ok:
            print(f"Szoba: {fogl.szoba.szobsz}, Időpont: {fogl.datum}")


hotel = Szalloda("Hotel Flamingó")

hotel.plus_szoba(EgyagyasSzoba("110", "Pezsgőfürdő"))
hotel.plus_szoba(EgyagyasSzoba("107", "Pezsgőfürdő"))
hotel.plus_szoba(EgyagyasSzoba("106", "Pezsgőfürdő"))
hotel.plus_szoba(EgyagyasSzoba("105", "Pezsgőfürdő"))
hotel.plus_szoba(EgyagyasSzoba("108", "Zuhanytemplom"))
hotel.plus_szoba(EgyagyasSzoba("109", "Zuhanytemplom"))
hotel.plus_szoba(EgyagyasSzoba("104", "Zuhanytemplom"))
hotel.plus_szoba(KetagyasSzoba("222", "InfraSzauna"))
hotel.plus_szoba(KetagyasSzoba("223", "InfraSzauna"))
hotel.plus_szoba(KetagyasSzoba("224", "InfraSzauna"))
hotel.plus_szoba(KetagyasSzoba("225", "InfraSzauna"))

hotel.fogl("110", datetime(2024, 8, 10))
hotel.fogl("108", datetime(2024, 8, 12))
hotel.fogl("222", datetime(2024, 8, 15))
hotel.fogl("110", datetime(2024, 8, 15))
hotel.fogl("108", datetime(2024, 8, 15))

while True:

    print("\nMit óhajt?:")
    print("1. Szoba lefoglalása")
    print("2. Foglalás lemondása")
    print("3. Foglalások kilistázása")
    print("4. Szobák kilistázása")
    print("5. Kilépés")
    case = input("Kérem választásszon a következő lehetőségek közül (1_2_3_4_5): ")

    if case == "1":
        szobsz = input("\nA lefoglalandó szoba száma: ")
        datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN, jelenleg csak egy napra lehetséges a foglalás): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            if datum < datetime.now():
                print("\nHibás dátum! A foglalás csak jövőbeni időpontra lehetséges.")

            else:
                ar = hotel.fogl(szobsz, datum)
                if ar:
                    print(f"A foglalás sikeres! Az ár: {ar} Ft")
                else:
                    print("\nHibás adat!")

        except ValueError:
            print("\nHibás a dátum formátuma!")
    elif case == "2":
        szobsz = input("\nLemondandó foglalás szoba száma?: ")
        datum = input("Lemondandó foglalás dátuma? (ÉÉÉÉ-HH-NN): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            siker = hotel.lemond(szobsz, datum)
            if siker:
                print("\nA foglalásod sikeresen lemondva.")
            else:
                print("\nNincs ilyen foglalás.")

        except ValueError:
            print("\nA dátum formátuma hibás!")

    elif case == "3":
        hotel.list_fogl_ok()
    elif case == "4":
        print("Szobák száma:")
        print(len(hotel.szobak))
        print("Egyágyas szobák:")
        for szoba in hotel.szobak:
            if isinstance(szoba, EgyagyasSzoba):
                print(f"Szobaszám: {szoba.szobsz}, Ár: {szoba.ar} Ft, (Fürdő: {szoba.bath})")
        print("\nKétágyas szobák:")
        for szoba in hotel.szobak:
            if isinstance(szoba, KetagyasSzoba):
                print(f"Szobaszám: {szoba.szobsz}, Ár: {szoba.ar} Ft, (Extra: {szoba.extra})")
    elif case == "5":
        break
    else:
        print("\nHibás választás!")
