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

SENSOR_ID = "sensor_001"

INTERVAL = 10

MIN_TEMPERATURE = 10.0
MAX_TEMPERATURE = 30.0

# Initial temperature
temperature = 22.0


def generate_temperature(current):
    """
    Change temperature by a random amount
    between -3 and +3 degrees.
    """

    change = random.uniform(-3.0, 3.0)

    new_temperature = current + change

    # Keep temperature within limits
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
        "battery_pct": round(random.uniform(70, 100), 2)
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
            f"Temperature: {reading['temperature_c']}°C | "
            f"Humidity: {reading['humidity_pct']}% | "
            f"Battery: {reading['battery_pct']}% | "
            f"Status: {response.status_code}",
            flush=True
        )

    except requests.RequestException as error:

        print(f"POST failed: {error}", flush=True)


def main():

    print("Sensor simulator started")
    print(f"Sensor ID: {SENSOR_ID}")
    print(f"Sending readings every {INTERVAL} seconds")
    print("----------------------------------------")

    while True:

        send_reading()

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()