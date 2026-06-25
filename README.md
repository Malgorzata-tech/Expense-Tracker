# Expense Manager (desktop application)

Menedżer wydatków z interfejsem graficznym opartym na Tkinter.

Szybkie instrukcje uruchomienia:
- Otwórz folder "expense-tracker" z projketem w terminalu i ruchom go: python main.py
- Jeśli środowisko ma zainstalowany Tkinter, otworzy się okno GUI do dodawania, filtrowania i przeglądania wydatków.

Uwagi o funkcjach:
- W podsumowaniu wydatków zapisywana jest data dodania (w chwili dodania wydatku).
- Występuje możliwość filtrowania wydatków po kategorii - kliknięcie przycisku "Filtruj po kategorii" (po wyborze kategorii z listy dostępnych).
- Aby odfiltrować wydatki należy kliknąć przycisk "Odfiltruj"
- Niepełne kwoty należy dodawać z kropką a nie z przecinkiem (np. 12.50 zamiast 12,50).
- Okno aplikacji jest zablokowane przed zmianą rozmiaru.



Instrukcje instalacji Tkinter

Windows:
  - Zazwyczaj Tkinter jest dołączony do instalatora Pythona ze strony python.org. 
	- Jeśli go brakuje, pobierz i zainstaluj najnowszego Pythona 
	- i podczas instalacji upewnij się, że zaznaczona jest opcja "tcl/tk and IDLE".
  - Alternatywnie spróbuj: pip install tk (może nie działać we wszystkich konfiguracjach).

Linux (Debian/Ubuntu):
  - Otwórz terminal i uruchom: sudo apt update && sudo apt install python3-tk -y

Po instalacji uruchom ponownie system (jeśli wymagane) i sprawdź: python -c "import tkinter; print(tkinter.TkVersion)". 
Jeśli polecenie nie zgłasza błędu i wypisuje numer wersji, Tkinter jest dostępny.
