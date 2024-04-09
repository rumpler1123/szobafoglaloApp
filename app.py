from abc import ABC, abstractmethod
from datetime import *
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Hozz létre egy Szoba absztrakt osztályt, amely alapvető attribútumokat definiál (ár, szobaszám). 
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def szobaInfo(self):
        pass

# Hozz létre az Szoba osztályból EgyagyasSzoba és KetagyasSzoba származtatott osztályokat
class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar=ar, szobaszam=szobaszam)
    
    def szobaInfo(self):
        return f"Egyágyas szoba, Ár:  {self.ar} Ft, Szobaszám: {self.szobaszam}"

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar=ar, szobaszam=szobaszam)
    
    def szobaInfo(self):
        return f"Kétágyas szoba, Ár:  {self.ar} Ft, Szobaszám: {self.szobaszam} "

# Hozz létre egy Szalloda osztályt, ami ezekből a Szobákból áll, és van saját attributuma is (név pl.)
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
    
    def szobaHozzaadasa(self, szoba):
        self.szobak.append(szoba)

    def foglalasHozzadasa(self, szobaszam, datum):
        self.foglalasok.append(Foglalas(szobaszam, datum))

    def szobakListazasa(self):
        szobaLista = ""
        for szoba in self.szobak:
            szobaLista += szoba.szobaInfo() + "\n"
        return szobaLista
    
# Hozz létre egy Foglalás osztályt, amelybe a Szálloda szobáinak foglalását tároljuk (elég itt, ha egy foglalás csak egy napra szól)
class Foglalas:
    def __init__(self, szobaszam, datum):
        self.szobaszam = szobaszam
        self.datum = datetime.strptime(datum, '%Y-%m-%d') 

    def info(self):
        return f"Szobaszám: {self.szobaszam}, Dátum: {self.datum.strftime('%Y-%m-%d')}"

# Implementálj egy metódust, ami lehetővé teszi szobák foglalását dátum alapján, visszaadja annak árát
def szobaFoglalas(szalloda, szobaszam, datum):
    szobaszam = szobaszam 
    datum = datum 
    maiDatum = date.today().strftime('%Y-%m-%d')
    # A foglalás létrehozásakor ellenőrizd, hogy a dátum érvényes (jövőbeni) és a szoba elérhető-e akkor.
    for foglalas in szalloda.foglalasok:
        foglalatDatum = foglalas.datum.strftime('%Y-%m-%d')
        if str(foglalas.szobaszam) == szobaszam and foglalatDatum == datum:
            return "A megadott napra a szoba már foglalt!"
        elif datum < maiDatum:
            return "A megadott dátum nem megfelelő!"

    for szoba in szalloda.szobak:
        if str(szoba.szobaszam) == szobaszam:
            szalloda.foglalasHozzadasa(szobaszam, datum)
            return f"siekres foglalas! A foglalás Ára: {szoba.ar} Ft"
    return "A megadott szobaszám nem létezik" 

# Implementálj egy metódust, ami lehetővé teszi a foglalás lemondását.
def foglalasLemondasa(szalloda, szobaszam, datum):
    szobaszam = szobaszam 
    datum = datum 
    #Biztosítsd, hogy a lemondások csak létező foglalásokra lehetségesek
    for foglalas in szalloda.foglalasok:
        foglalatDatum = foglalas.datum.strftime('%Y-%m-%d')
        if str(foglalas.szobaszam) == szobaszam and foglalatDatum == datum:
            szalloda.foglalasok.remove(foglalas)
            return "sikeres lemondás!"
    return "Sikertelen lemondás! A megadott szobaszám vagy dátum helytelen!"

# Implementálj egy metódust, ami listázza az összes foglalást.
def foglalasokListazasa(szalloda):
    foglalasokLista = ""
    if not szalloda.foglalasok:
        return "Nincsenek foglalások."
    for foglalas in szalloda.foglalasok:
        foglalasokLista += foglalas.info() + "\n"
    return foglalasokLista


# Töltsd fel az futtatás után a rendszert 1 szállodával, 3 szobával és 5 foglalással, mielőtt a felhasználói adatbekérés megjelenik.
def szallodaFeltoltese(szalloda, egyagyas, ketagyas):
    szalloda.szobaHozzaadasa(EgyagyasSzoba(egyagyas,1022))
    szalloda.szobaHozzaadasa(EgyagyasSzoba(egyagyas,2022))
    szalloda.szobaHozzaadasa(KetagyasSzoba(ketagyas,4022))

    szalloda.foglalasHozzadasa(1022, "2024-06-29")
    szalloda.foglalasHozzadasa(2022, "2024-06-20")
    szalloda.foglalasHozzadasa(2022, "2024-06-03")
    szalloda.foglalasHozzadasa(1022, "2024-06-13")
    szalloda.foglalasHozzadasa(4022, "2024-09-23")

# Készíts egy egyszerű felhasználói interfészt, ahol a felhasználó kiválaszthatja a kívánt műveletet (pl. foglalás, lemondás, listázás).
class SzallodaUI:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.root = tk.Tk()
        self.root.title(szalloda.nev)
        
        # Szobák szövegdoboz
        szobak_frame = tk.Frame(self.root)
        szobak_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(szobak_frame, text="Szobák listája: ").pack()
        self.szobak_txt = scrolledtext.ScrolledText(szobak_frame, height=5, width=50)
        self.szobak_txt.pack(pady=5)

        # Foglalások szövegdoboz
        foglalasok_frame = tk.Frame(self.root)
        foglalasok_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(foglalasok_frame, text="Foglalások listája: ").pack()
        self.foglalasok_txt = scrolledtext.ScrolledText(foglalasok_frame, height=10, width=50)
        self.foglalasok_txt.pack(pady=5)

        # Gombok
        gombok_frame = tk.Frame(self.root)
        gombok_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Button(gombok_frame, text="Szobák Listázása", command=self.szobak_listazasa).pack(fill=tk.X, pady=5)
        tk.Button(gombok_frame, text="Foglalások Listázása", command=self.foglalasok_listazasa).pack(fill=tk.X, pady=5)
        tk.Button(gombok_frame, text="Új foglalás", command=self.szoba_foglalas).pack(fill=tk.X, pady=5)
        tk.Button(gombok_frame, text="Foglalás Lemondása", command=self.foglalas_lemondasa).pack(fill=tk.X, pady=5)

    def run(self):
        self.root.mainloop()

    # Funkciók 
    def szobak_listazasa(self):
        self.szobak_txt.delete('1.0', tk.END)  
        szoba_lista = "\n".join([szalloda.szobakListazasa()])
        self.szobak_txt.insert(tk.END, szoba_lista)

    def foglalasok_listazasa(self):
        self.foglalasok_txt.delete('1.0', tk.END)
        foglalas_lista = "\n".join([foglalasokListazasa(szalloda)])
        self.foglalasok_txt.insert(tk.END, foglalas_lista)

    def szoba_foglalas(self):
        szobaszam = simpledialog.askstring("Új Foglalás", "Szobaszám:")
        datum = simpledialog.askstring("Új Foglalás", "Dátum (ÉÉÉÉ-HH-NN):")
        uzenet = szobaFoglalas(self.szalloda, szobaszam, datum)
        messagebox.showinfo("Foglalás Eredménye", uzenet)

    def foglalas_lemondasa(self):
        szobaszam = simpledialog.askstring("Foglalás Lemondása", "Szobaszám:")
        datum = simpledialog.askstring("Foglalás Lemondása", "Dátum (ÉÉÉÉ-HH-NN):")
        uzenet = foglalasLemondasa(self.szalloda, szobaszam, datum)
        messagebox.showinfo("Lemondás Eredménye", uzenet)



szalloda = Szalloda("Teszt Hotel")
szallodaFeltoltese(szalloda, 10000, 30000)
app = SzallodaUI(szalloda)
app.run()