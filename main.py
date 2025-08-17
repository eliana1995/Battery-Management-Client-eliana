import time
from utils import get_info, get_baseload, get_prices, start_charging, stop_charging

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

def main():
    charging = False
    prices = get_prices()
    baseload = get_baseload()

    for hour in range(24):
        info = get_info()

        if info is None:
            print("Fel: Kan inte hämta data från servern, försöker igen...")
            time.sleep(4)
            continue

        if 'battery_capacity_kWh' not in info or 'base_current_load' not in info:
            print(f"Fel: Saknad data i serverns svar: {info}")
            time.sleep(4)
            continue

        battery_kwh = info['battery_capacity_kWh']
        current_load = info['base_current_load']
        percent = get_battery_percentage(battery_kwh)
        price = prices.get(str(hour), None)
        household = baseload.get(str(hour), None)

        if price is None or household is None:
            print(f"Fel: Saknad pris eller hushållsdata för timme {hour}")
            time.sleep(4)
            continue

        print(f"Timme {hour:02d}: Elpris = {price} öre/kWh, Hushållsförbrukning = {household} kW, Batteri = {percent}%")

        if 20 <= percent < 80 and current_load < 11:
            if household == min(map(float, baseload.values())):
                if not charging:
                    print("→ Startar laddning (lägsta hushållsförbrukning)")
                    start_charging()
                    charging = True
            elif price == min(map(float, prices.values())):
                if not charging:
                    print("→ Startar laddning (lägsta elpris)")
                    start_charging()
                    charging = True
        else:
            if charging:
                print("→ Stoppar laddning")
                stop_charging()
                charging = False

        print("-" * 40)
        time.sleep(4)  # 1 timme simuleras som 4 sekunder

if __name__ == "__main__":
    main()

