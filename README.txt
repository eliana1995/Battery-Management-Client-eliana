Battery Management Client – Python

Körning:
1. Installera beroenden:
   pip install -r requirements.txt

2. Starta laddstationsservern i annan terminal.

3. Kör terminalversion:
   python main.py

4. Kör GUI-version:
   python gui.py

Denna klient laddar batteriet från 20% till 80% endast när elpriset eller hushållsförbrukningen är som lägst och total förbrukning < 11 kW.