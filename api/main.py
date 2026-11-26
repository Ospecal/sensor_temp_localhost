
import os
import psycopg

from psycopg.rows import dict_row
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, Header, Query, Response, status


from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

app = FastAPI(title="Sensor Readings API", version="2.0")

# Configuration
DATABASE_URL = os.environ["DATABASE_URL"]
API_TOKEN = os.environ["API_TOKEN"]

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Authentication

def verify_token(
        authorization: Annotated[str | None, Header()] = None
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization"
        )

    token = authorization[7:]

    import hmac

    if not hmac.compare_digest(token, API_TOKEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )


# Database

def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


# Data model

# class SensorReading(BaseModel):
#     sensor_id: str
#     measured_at: datetime
#     temperature_c: float | None = None
#     humidity_pct: float | None = Field(default=None, ge= 0, le = 100)
#     battery_pct: float | None = Field(default=None, ge= 0, le = 100)

class SensorReading(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sensor_id: str = Field(min_length=1, max_length=100)
    measured_at: datetime

    temperature_c: float | None = None
    humidity_pct: float | None = Field(default=None, ge=0, le=100)
    battery_pct: float | None = Field(default=None, ge=0, le=100)

    light_lux: float | None = Field(default=None, ge=0)
    pir: bool | None = None
    co2_ppm: float | None = Field(default=None, ge=0)
    tvoc_ppb: float | None = Field(default=None, ge=0)
    pressure_hpa: float | None = Field(default=None, gt=0)
    pm25_ugm3: float | None = Field(default=None, ge=0)
    pm10_ugm3: float | None = Field(default=None, ge=0)


# class SensorReadingUpdate(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     sensor_id: str | None = Field(default=None, min_length=1, max_length=100)
#     measured_at: datetime | None = None
#     temperature_c: float | None = None
#     humidity_pct: float | None = Field(default=None, ge=0, le=100)
#     battery_pct: float | None = Field(default=None, ge=0, le=100)

class SensorReadingUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sensor_id: str | None = Field(default=None, min_length=1, max_length=100)
    measured_at: datetime | None = None

    temperature_c: float | None = None
    humidity_pct: float | None = Field(default=None, ge=0, le=100)
    battery_pct: float | None = Field(default=None, ge=0, le=100)

    light_lux: float | None = Field(default=None, ge=0)
    pir: bool | None = None
    co2_ppm: float | None = Field(default=None, ge=0)
    tvoc_ppb: float | None = Field(default=None, ge=0)
    pressure_hpa: float | None = Field(default=None, gt=0)
    pm25_ugm3: float | None = Field(default=None, ge=0)
    pm10_ugm3: float | None = Field(default=None, ge=0)




# Health
@app.get("/")
def home():
    return {"message": "Sensor API is running"}

@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")

        return {"status": "healthy"}

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

# GET: ALL readings

@app.get("/readings", dependencies=[Depends(verify_token)])
def get_readings(
    limit: int = Query(default=1000, ge=1, le=1000),
    offset: int = Query(default=0, ge=0)
):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM sensor_readings
                ORDER BY measured_at DESC, id DESC
                LIMIT %s OFFSET %s
            """, (limit, offset))

            return cur.fetchall()


# All sensors latest readings


@app.get("/readings/latest", dependencies=[Depends(verify_token)])
def get_latest_readings():

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT ON (sensor_id) *
                FROM sensor_readings
                ORDER BY sensor_id, measured_at DESC, id DESC
            """)

            return cur.fetchall()


# Show a single reading

@app.get("/readings/{reading_id}", dependencies=[Depends(verify_token)])
def get_reading(reading_id: int):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM sensor_readings
                WHERE id = %s
            """, (reading_id,))

            reading = cur.fetchone()

            if reading is None:
                raise HTTPException(404, "Reading not found")

            return reading


# POST create a reating

# @app.post("/readings", dependencies=[Depends(verify_token)])
# def create_reading(reading: SensorReading):

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

#             return cur.fetchone()

@app.post("/readings", dependencies=[Depends(verify_token)])
def create_reading(reading: SensorReading):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sensor_readings (
                    sensor_id,
                    measured_at,
                    temperature_c,
                    humidity_pct,
                    battery_pct,
                    light_lux,
                    pir,
                    co2_ppm,
                    tvoc_ppb,
                    pressure_hpa,
                    pm25_ugm3,
                    pm10_ugm3
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (
                reading.sensor_id,
                reading.measured_at,
                reading.temperature_c,
                reading.humidity_pct,
                reading.battery_pct,
                reading.light_lux,
                reading.pir,
                reading.co2_ppm,
                reading.tvoc_ppb,
                reading.pressure_hpa,
                reading.pm25_ugm3,
                reading.pm10_ugm3
            ))

            return cur.fetchone()

        
# PUT, replace a complete reading

# @app.put("/readings/{reading_id}", dependencies=[Depends(verify_token)])
# def replace_reading(
#     reading_id: int,
#     reading: SensorReading
# ):

#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 UPDATE sensor_readings
#                 SET
#                     sensor_id = %s,
#                     measured_at = %s,
#                     temperature_c = %s,
#                     humidity_pct = %s,
#                     battery_pct = %s
#                 WHERE id = %s
#                 RETURNING *
#             """, (
#                 reading.sensor_id,
#                 reading.measured_at,
#                 reading.temperature_c,
#                 reading.humidity_pct,
#                 reading.battery_pct,
#                 reading_id
#             ))

#             result = cur.fetchone()

#             if result is None:
#                 raise HTTPException(404, "Reading not found")

#             return result

@app.put("/readings/{reading_id}", dependencies=[Depends(verify_token)])
def replace_reading(
    reading_id: int,
    reading: SensorReading
):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE sensor_readings
                SET
                    sensor_id = %s,
                    measured_at = %s,
                    temperature_c = %s,
                    humidity_pct = %s,
                    battery_pct = %s,
                    light_lux = %s,
                    pir = %s,
                    co2_ppm = %s,
                    tvoc_ppb = %s,
                    pressure_hpa = %s,
                    pm25_ugm3 = %s,
                    pm10_ugm3 = %s
                WHERE id = %s
                RETURNING *
            """, (
                reading.sensor_id,
                reading.measured_at,
                reading.temperature_c,
                reading.humidity_pct,
                reading.battery_pct,
                reading.light_lux,
                reading.pir,
                reading.co2_ppm,
                reading.tvoc_ppb,
                reading.pressure_hpa,
                reading.pm25_ugm3,
                reading.pm10_ugm3,
                reading_id
            ))

            result = cur.fetchone()

            if result is None:
                raise HTTPException(404, "Reading not found")

            return result
        

# PATCH, to uptade selected fields

@app.patch("/readings/{reading_id}", dependencies=[Depends(verify_token)])
def update_reading(
    reading_id: int,
    reading: SensorReadingUpdate
):

    updates = reading.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(400, "No fields supplied")

    if "sensor_id" in updates and updates["sensor_id"] is None:
        raise HTTPException(422, "sensor_id cannot be null")

    if "measured_at" in updates and updates["measured_at"] is None:
        raise HTTPException(422, "measured_at cannot be null")

    allowed_fields = {
        "sensor_id",
        "measured_at",
        "temperature_c",
        "humidity_pct",
        "battery_pct",
        "light_lux",
        "pir",
        "co2_ppm",
        "tvoc_ppb",
        "pressure_hpa",
        "pm25_ugm3",
        "pm10_ugm3"
    }

    fields = [field for field in updates if field in allowed_fields]

    set_clause = ", ".join(
        f"{field} = %s" for field in fields
    )

    values = [updates[field] for field in fields]
    values.append(reading_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE sensor_readings
                SET {set_clause}
                WHERE id = %s
                RETURNING *
            """, values)

            result = cur.fetchone()

            if result is None:
                raise HTTPException(404, "Reading not found")

            return result




# DELETE, delete a reading
    
@app.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_token)]
)
def delete_reading(reading_id: int):

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM sensor_readings
                WHERE id = %s
                RETURNING id
            """, (reading_id,))

            if cur.fetchone() is None:
                raise HTTPException(404, "Reading not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


