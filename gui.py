import tkinter as tk
from tkinter import ttk
from utils import get_info, start_charging, stop_charging

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

class BatteryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EV Batterihantering")
        self.geometry("350x300")

        self.battery_label = ttk.Label(self, text="Batteri: -- %")
        self.battery_label.pack(pady=10)

        self.info_text = tk.Text(self, height=10, width=40)
        self.info_text.pack()

        self.btn_start = ttk.Button(self, text="Starta laddning", command=self.start_charge)
        self.btn_start.pack(pady=5)

        self.btn_stop = ttk.Button(self, text="Stoppa laddning", command=self.stop_charge)
        self.btn_stop.pack(pady=5)

        self.update_info()

    def update_info(self):
        info = get_info()
        if info:
            percent = get_battery_percentage(info['battery_capacity_kWh'])
            self.battery_label.config(text=f"Batterinivå: {percent} %")

            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Tid: {info['sim_time_hour']:02d}:{info['sim_time_min']:02d}\n")
            self.info_text.insert(tk.END, f"Hushållsförbrukning: {info['base_current_load']} kW\n")
            self.info_text.insert(tk.END, f"Laddning på: {'Ja' if info['charging_enabled'] else 'Nej'}\n")
        else:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Fel: Kan ej hämta data från servern")

        self.after(3000, self.update_info)  # Uppdatera varje 3 sekunder

    def start_charge(self):
        start_charging()
        self.update_info()

    def stop_charge(self):
        stop_charging()
        self.update_info()

if __name__ == "__main__":
    app = BatteryApp()
    app.mainloop()
