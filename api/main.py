
import os
import psycopg

from psycopg.rows import dict_row
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Sensor Readings API")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


# Data model
class SensorReading(BaseModel):
    sensor_id: str
    measured_at: datetime
    temperature_c: float | None = None
    humidity_pct: float | None = None
    battery_pct: float | None = None


@app.get("/")
def home():
    return {"message": "Sensor API is running"}




@app.get("/readings")
def get_readings():

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM sensor_readings
                ORDER BY measured_at DESC
            """)

            return cur.fetchall()


@app.get("/readings/latest")
def get_latest_readings():

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (sensor_id) *
                FROM sensor_readings
                ORDER BY sensor_id, measured_at DESC, id DESC
            """)

            return cur.fetchall()

@app.post("/readings")
def create_reading(reading: SensorReading):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sensor_readings (
                    sensor_id,
                    measured_at,
                    temperature_c,
                    humidity_pct,
                    battery_pct
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (
                reading.sensor_id,
                reading.measured_at,
                reading.temperature_c,
                reading.humidity_pct,
                reading.battery_pct
            ))

            return cur.fetchone()


# import os
# import hmac

# import psycopg
# from psycopg.rows import dict_row

# from fastapi import FastAPI, Header, HTTPException
# from pydantic import BaseModel
# from datetime import datetime


# app = FastAPI(title="Sensor Readings API")

# DATABASE_URL = os.environ["DATABASE_URL"]
# API_TOKEN = os.environ["API_TOKEN"]


# class SensorReading(BaseModel):
#     sensor_id: str
#     measured_at: datetime
#     temperature_c: float | None = None
#     humidity_pct: float | None = None
#     battery_pct: float | None = None


# def get_connection():
#     return psycopg.connect(
#         DATABASE_URL,
#         row_factory=dict_row
#     )


# def authenticate(authorization: str | None):
#     expected = f"Bearer {API_TOKEN}"

#     if not authorization or not hmac.compare_digest(
#         authorization, expected
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Unauthorized"
#         )


# @app.get("/")
# def home():
#     return {"message": "Sensor API is running"}


# @app.get("/readings")
# def get_readings():
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT *
#                 FROM sensor_readings
#                 ORDER BY measured_at DESC
#             """)
#             return cur.fetchall()


# @app.post("/readings")
# def create_reading(
#     reading: SensorReading,
#     authorization: str | None = Header(default=None)
# ):
#     authenticate(authorization)

#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO sensor_readings (
#                     sensor_id,
#                     measured_at,
#                     temperature_c,
#                     humidity_pct,
#                     battery_pct
#                 )
#                 VALUES (%s, %s, %s, %s, %s)
#                 RETURNING *
#             """, (
#                 reading.sensor_id,
#                 reading.measured_at,
#                 reading.temperature_c,
#                 reading.humidity_pct,
#                 reading.battery_pct
#             ))

#             result = cur.fetchone()

#     return result


# @app.get("/readings/latest")
# def get_latest_readings():
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 SELECT DISTINCT ON (sensor_id)
#                     *
#                 FROM sensor_readings
#                 ORDER BY sensor_id, measured_at DESC, id DESC
#             """)
#             return cur.fetchall()
