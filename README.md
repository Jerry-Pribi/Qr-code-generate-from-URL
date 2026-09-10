QR Code Generator

Jednoduchá desktopová aplikace v Pythonu s grafickým rozhraním (Tkinter + CustomTkinter), která ze zadané URL adresy vygeneruje QR kód, umožní ho stáhnout jako obrázek a ukládá historii generovaných kódů do lokální SQLite databáze.

Funkce
Zadání URL adresy (pokud chybí http:///https://, doplní se automaticky https://)
Kontrola, zda je URL platná a dostupná (ověření pomocí knihovny requests)
Vygenerování QR kódu z platné URL a jeho zobrazení v okně aplikace
Zadání vlastního názvu souboru pro uložení QR kódu
Stažení vygenerovaného QR kódu do složky Downloads ve formátu .jpg
Automatické zabránění přepsání existujícího souboru (přidání _1, _2, ...)
Zobrazení chybových hlášek při neplatném vstupu
Ukládání historie vygenerovaných QR kódů do SQLite databáze (QR-code-history.db)
Sledování, zda byl konkrétní QR kód stažený (sloupec download, hodnota 0/1)
Požadavky
Python 3.8+
Knihovny:
customtkinter
requests
qrcode
Pillow
sqlite3 – součást standardní knihovny Pythonu, není potřeba instalovat zvlášť
Instalace
bash
pip install customtkinter requests qrcode pillow

Poznámka: tkinter je součástí standardní instalace Pythonu na většině systémů (na Linuxu může být potřeba doinstalovat balíček python3-tk).

Spuštění
bash
python gui_qr.py

Při prvním spuštění se ve stejné složce automaticky vytvoří soubor QR-code-history.db s tabulkou historie.

Použití
Do pole Enter URL zadej webovou adresu.
Do pole Name in folder zadej název, pod kterým se má soubor uložit.
Klikni na Generate – aplikace ověří dostupnost URL, vygeneruje QR kód a uloží záznam do databáze (zatím jako nestažený).
Klikni na Download – QR kód se uloží do složky ~/Downloads jako .jpg a v databázi se u příslušného záznamu nastaví, že byl stažený.
Struktura databáze

Tabulka historie v souboru QR-code-history.db:

Sloupec	Typ	Popis
id	INTEGER	Primární klíč, automaticky se zvyšuje
url	TEXT	Zadaná URL adresa
name_file	TEXT	Název souboru zadaný uživatelem
date	TEXT	Datum vygenerování (formát RRRR-M-D)
download	INTEGER	0 = nestaženo, 1 = staženo

Obsah databáze lze prohlížet a upravovat například nástrojem DB Browser for SQLite.

Struktura projektu
gui_qr.py             # hlavní a jediný soubor aplikace
QR-code-history.db     # SQLite databáze historie (vytvoří se automaticky)
Možná vylepšení do budoucna
Přidat výběr formátu (PNG, SVG) a barvy QR kódu
Umožnit výběr cílové složky pro uložení
Validace URL bez nutnosti síťového dotazu (offline režim)
Náhled QR kódu ve větším rozlišení
Lepší formátování rozložení (aktuálně pevné souřadnice place())
Zobrazit historii generovaných QR kódů přímo v okně aplikace (např. tabulka/seznam)
Možnost smazat záznam z historie přímo z GUI
Filtrování/vyhledávání v historii podle URL nebo data
Zaokrouhlit formát data na RRRR-MM-DD (doplnit nuly u měsíce/dne)
