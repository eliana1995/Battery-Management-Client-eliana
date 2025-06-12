import tkinter as tk
from tkinter import ttk
from utils import get_info, get_baseload, get_prices, start_charging, stop_charging

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

class BatteryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battery Management Client")
        self.geometry("400x400")
        
        self.battery_label = ttk.Label(self, text="Batterinivå: -- %")
        self.battery_label.pack(pady=10)
        
        self.info_text = tk.Text(self, height=15, width=50)
        self.info_text.pack()

        self.refresh_button = ttk.Button(self, text="Uppdatera Info", command=self.update_info)
        self.refresh_button.pack(pady=5)

        self.charge_button = ttk.Button(self, text="Starta Laddning", command=start_charging)
        self.charge_button.pack(pady=5)

        self.stop_button = ttk.Button(self, text="Stoppa Laddning", command=stop_charging)
        self.stop_button.pack(pady=5)

        self.update_info()

    def update_info(self):
        info = get_info()
        prices = get_prices()
        baseload = get_baseload()

        battery_percent = get_battery_percentage(info['ev_battery'])
        self.battery_label.config(text=f"Batterinivå: {battery_percent}%")

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Totalförbrukning: {info['total_consumption']} kW\n")
        self.info_text.insert(tk.END, f"Timmarspriser:\n")

        for hour, price in prices.items():
            self.info_text.insert(tk.END, f"{hour}:00 - {price} öre/kWh\n")

        self.info_text.insert(tk.END, "\nBaseload (hushåll):\n")
        for hour, load in baseload.items():
            self.info_text.insert(tk.END, f"{hour}:00 - {load} kW\n")

if __name__ == "__main__":
    app = BatteryApp()
    app.mainloop()