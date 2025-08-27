import time
from utils import get_info, get_baseload, get_prices, start_charging, stop_charging

def get_battery_percentage(kwh, max_kwh=40):
    return round((kwh / max_kwh) * 100, 1)

def main():
    charging = False

    price = get_prices()

    if not price:
        print(" Kunde inte hämta elpriser från servern. Avbryter.")
        return

    baseload = get_baseload()
    if not baseload:
        print(" Kunde inte hämta hushållsförbrukning. Avbryter.")
        return

    print(" Priser och hushållsdata hämtade. Startar simulering...\n")

    while True:
        info = get_info()

        if info is None:
            print("  Fel: Kan inte hämta data från servern, försöker igen...")
            time.sleep(4)
            continue

        hour = info.get("sim_time_hour")
        battery_kwh = info.get('battery_capacity_kWh')
        current_load = info.get('base_current_load_kW')
        percent = get_battery_percentage(battery_kwh)
        price = price.get(str(hour))
        household = baseload.get(str(hour))

        if price is None or household is None:
            print(f" Fel: Saknad pris eller hushållsdata för timme {hour}")
            time.sleep(4)
            continue

        print(f" Timme {hour:02d}: Elpris = {price} öre/kWh, Hushåll = {household} kW, Batteri = {percent}%")

        if 20 <= percent < 80 and current_load < 11:
            if float(household) == min(map(float, baseload.values())):
                reason = "lägsta hushållsförbrukning"
            elif float(price) == min(map(float, prices.values())):
                reason = "lägsta elpris"
            else:
                reason = None

            if reason and not charging:
                print(f"→ Startar laddning ({reason})")
                start_charging()
                charging = True
        else:
            if charging:
                print("→ Stoppar laddning")
                stop_charging()
                charging = False

        print("-" * 40)
        time.sleep(4)  # Simulerar 1 timme som 4 sekunder

if __name__ == "__main__":
    main()
