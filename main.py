import time
from utils import get_info, get_baseload, get_prices, start_charging, stop_charging

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

def main():
    baseload = get_baseload()
    prices = get_prices()
    charging = False

    for hour in range(24):
        info = get_info()
        current_kwh = info['ev_battery']
        battery_percent = get_battery_percentage(current_kwh)
        total_consumption = info['total_consumption']
        price = prices[str(hour)]
        household = baseload[str(hour)]

        print(f"Hour {hour}:")
        print(f"  Price: {price} öre/kWh")
        print(f"  Household Consumption: {household} kW")
        print(f"  Total Consumption: {total_consumption} kW")
        print(f"  Battery: {battery_percent}%")

        if 20 <= battery_percent < 80 and total_consumption < 11:
            if household == min([float(v) for v in baseload.values()]):
                print("  -> Starting charge (Del 1)")
                start_charging()
                charging = True
            elif price == min([float(p) for p in prices.values()]):
                print("  -> Starting charge (Del 2)")
                start_charging()
                charging = True
        else:
            if charging:
                print("  -> Stopping charge")
                stop_charging()
                charging = False

        print("-" * 40)
        time.sleep(0.5)

if __name__ == "__main__":
    main()