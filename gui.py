import tkinter as tk
from tkinter import ttk, scrolledtext
from utils import get_info, start_charging, stop_charging, get_prices

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

class BatteryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EV Batterihantering")
        self.geometry("420x600")
        self.resizable(False, False)

        # Batterinivå
        self.battery_label = ttk.Label(self, text="Batterinivå: -- %", font=("Helvetica", 14))
        self.battery_label.pack(pady=10)

        # Info-text
        self.info_text = scrolledtext.ScrolledText(self, height=6, width=50, state='normal')
        self.info_text.pack(pady=5)

        # Pris-label
        self.price_label = ttk.Label(self, text="Elpriser (öre/kWh) per timme:", font=("Helvetica", 12))
        self.price_label.pack(pady=5)

        # Pris-text med scrollbar
        self.price_text = scrolledtext.ScrolledText(self, height=10, width=50, state='normal')
        self.price_text.pack(pady=5)

        # Start/Stop-knappar
        self.btn_start = ttk.Button(self, text="Starta laddning", command=self.start_charge)
        self.btn_start.pack(pady=5)

        self.btn_stop = ttk.Button(self, text="Stoppa laddning", command=self.stop_charge)
        self.btn_stop.pack(pady=5)

        # Börja uppdatera UI
        self.update_info()

    def update_info(self):
        info = get_info()
        prices = get_prices()

        # Uppdatera batterinivå och status
        if info:
            percent = get_battery_percentage(info.get('battery_capacity_kWh', 0))
            self.battery_label.config(text=f"Batterinivå: {percent} %")

            sim_hour = info.get('sim_time_hour', "--")
            sim_min = info.get('sim_time_min', "--")
            load = info.get('base_current_load_kW', "--")
            charging = info.get('charging_enabled', False)

            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Tid: {sim_hour:02d}:{sim_min:02d}\n")
            self.info_text.insert(tk.END, f"Hushållsförbrukning: {load} kW\n")
            self.info_text.insert(tk.END, f"Laddning på: {'Ja' if charging else 'Nej'}\n")
        else:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, " Fel: Kunde inte hämta info från servern")

        # Uppdatera priser
        self.price_text.delete(1.0, tk.END)
        if prices:
            for hour in range(24):
                price = prices.get(str(hour), "N/A")
                self.price_text.insert(tk.END, f"Timme {hour:02d}: {price} öre/kWh\n")
        else:
            self.price_text.insert(tk.END, " Fel: Kunde inte hämta elpriser")

        # Kör om 3 sekunder
        self.after(3000, self.update_info)

    def start_charge(self):
        start_charging()
        self.update_info()

    def stop_charge(self):
        stop_charging()
        self.update_info()

if __name__ == "__main__":
    app = BatteryApp()
    app.mainloop()
