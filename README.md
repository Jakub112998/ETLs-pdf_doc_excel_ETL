# Overwiew:
Solution is to list the files and then load them in parallel 
process them, merge them and get the counts with all nuts and 
bolts in place.

# Extract
Factory pattern - różne źródła.
TODO: detekcja formatu
      

# Transform
- most of subjects/sections in csv files mają czcionkę >= 11 oraz pogrubone
	- nie zawierają więcej niż 1 kropkę i/lub jest dwukropek (jeśli dwukropek to tytuł zwykle po nim) oraz;
	- zwykle w tym wierszu nie ma nic więcej niż tekst w tej jednej komórce oraz;
	- znajduje się tam słowo "część" lub "pakiet" lub "nr"
	- z pliku należy ekstrachować jedynie tabelę.

# Load