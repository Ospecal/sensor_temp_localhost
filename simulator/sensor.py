
# import os
# import time
# import random
# import requests

# from datetime import datetime, timezone


# # Configuration
# API_URL = os.getenv(
#     "API_URL",
#     "http://localhost:8080/readings"
# )

# API_TOKEN = os.environ["API_TOKEN"]

# SENSOR_ID = "sensor_001"

# INTERVAL = 10

# MIN_TEMPERATURE = 10.0
# MAX_TEMPERATURE = 30.0

# # Initial temperature
# temperature = 22.0


# def generate_temperature(current):
#     """
#     Change temperature by a random amount
#     between -3 and +3 degrees.
#     """

#     change = random.uniform(-3.0, 3.0)

#     new_temperature = current + change

#     # Keep temperature within limits
#     new_temperature = max(
#         MIN_TEMPERATURE,
#         min(MAX_TEMPERATURE, new_temperature)
#     )

#     return round(new_temperature, 2)


# def generate_reading():

#     global temperature

#     temperature = generate_temperature(temperature)

#     reading = {
#         "sensor_id": SENSOR_ID,
#         "measured_at": datetime.now(timezone.utc).isoformat(),
#         "temperature_c": temperature,
#         "humidity_pct": round(random.uniform(30, 80), 2),
#         "battery_pct": round(random.uniform(70, 100), 2)
#     }

#     return reading


# def send_reading():

#     reading = generate_reading()

#     headers = {
#         "Authorization": f"Bearer {API_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     try:

#         response = requests.post(
#             API_URL,
#             json=reading,
#             headers=headers,
#             timeout=5
#         )

#         response.raise_for_status()

#         print(
#             f"[{reading['measured_at']}] "
#             f"Temperature: {reading['temperature_c']}°C | "
#             f"Humidity: {reading['humidity_pct']}% | "
#             f"Battery: {reading['battery_pct']}% | "
#             f"Status: {response.status_code}",
#             flush=True
#         )

#     except requests.RequestException as error:

#         print(f"POST failed: {error}", flush=True)


# def main():

#     print("Sensor simulator started")
#     print(f"Sensor ID: {SENSOR_ID}")
#     print(f"Sending readings every {INTERVAL} seconds")
#     print("----------------------------------------")

#     while True:

#         send_reading()

#         time.sleep(INTERVAL)


# if __name__ == "__main__":
#     main()

import os
import time
import random
import requests

from datetime import datetime, timezone


# Configuration
API_URL = os.getenv(
    "API_URL",
    "http://localhost:8080/readings"
)

API_TOKEN = os.environ["API_TOKEN"]

SENSOR_ID = "am308_001"

INTERVAL = 10

MIN_TEMPERATURE = 10.0
MAX_TEMPERATURE = 30.0

temperature = 22.0


def generate_temperature(current):
    change = random.uniform(-1.0, 1.0)

    new_temperature = current + change

    new_temperature = max(
        MIN_TEMPERATURE,
        min(MAX_TEMPERATURE, new_temperature)
    )

    return round(new_temperature, 2)


def generate_reading():

    global temperature

    temperature = generate_temperature(temperature)

    reading = {
        "sensor_id": SENSOR_ID,
        "measured_at": datetime.now(timezone.utc).isoformat(),

        "temperature_c": temperature,
        "humidity_pct": round(random.uniform(30, 80), 2),
        "battery_pct": round(random.uniform(70, 100), 2),

        "light_lux": round(random.uniform(0, 1000), 2),
        "pir": random.random() < 0.1,
        "co2_ppm": round(random.uniform(400, 1500), 2),
        "tvoc_ppb": round(random.uniform(0, 600), 2),
        "pressure_hpa": round(random.uniform(980, 1030), 2),
        "pm25_ugm3": round(random.uniform(0, 50), 2),
        "pm10_ugm3": round(random.uniform(0, 100), 2)
    }

    return reading


def send_reading():

    reading = generate_reading()

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            API_URL,
            json=reading,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        print(
            f"[{reading['measured_at']}] "
            f"Temp: {reading['temperature_c']}°C | "
            f"Humidity: {reading['humidity_pct']}% | "
            f"Light: {reading['light_lux']} lux | "
            f"PIR: {reading['pir']} | "
            f"CO2: {reading['co2_ppm']} ppm | "
            f"TVOC: {reading['tvoc_ppb']} ppb | "
            f"Pressure: {reading['pressure_hpa']} hPa | "
            f"PM2.5: {reading['pm25_ugm3']} | "
            f"PM10: {reading['pm10_ugm3']} | "
            f"Battery: {reading['battery_pct']}% | "
            f"Status: {response.status_code}",
            flush=True
        )

    except requests.RequestException as error:

        print(f"POST failed: {error}", flush=True)


def main():

    print("AM308 simulator started")
    print(f"Sensor ID: {SENSOR_ID}")
    print(f"Sending readings every {INTERVAL} seconds")
    print("----------------------------------------")

    while True:

        send_reading()

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()