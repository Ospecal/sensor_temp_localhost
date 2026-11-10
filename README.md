
# Sensor Readings API – PostgreSQL Docker Environment

A small test environment for storing and retrieving sensor readings using PostgreSQL, FastAPI, Docker Compose, DBeaver, and Postman.

The project provides a REST API that allows users to submit sensor readings to a PostgreSQL database and retrieve historical or latest readings.

## Starting the environment:
Open a terminal in the root directory containing docker-compose.yml.
### Step 1 – Build and start the containers
bash <br>
To start the container:
<pre>
docker compose up -d
</pre>
To rebuild and start the container:
<pre>
docker compose up -d --build
</pre>
This command:

    Downloads the PostgreSQL image if necessary.
    Builds the FastAPI Docker image.
    Creates the database container.
    Creates the API container.
    Starts both services.

To stop the container:
<pre>
docker compose down
</pre>
to delete containers:
<pre>
docker compose down -v
</pre>
### Step 2 – Check container status
bash
<pre>
docker compose ps
</pre>
Both containers should be running.
### Step 3 – Check the logs
bash
<pre>
docker compose logs -f
</pre>
To inspect only the API:
<pre>
docker compose logs -f api
</pre>
To inspect only PostgreSQL:
<pre>
docker compose logs -f db
</pre>

## Step 4 – Verify the API

Open the following URL in your browser:

http://localhost:8080/

Expected response:
<pre>
{
    "message": "Sensor API is running"
}
</pre>
You can also access the automatically generated FastAPI documentation:

http://localhost:8080/docs

## Connecting to PostgreSQL Using DBeaver

Open DBeaver and create a new PostgreSQL connection.

Use the following connection settings:
| Setting	| Value |
| --------- | --------- |
| Host	| localhost |
| Port	| 5433 |
| Database	| appdb |
| Username	| app |
| Password	| sensor |

Click Test Connection and then Finish.

Once connected, navigate to:
<pre>
appdb
  └── Schemas
       └── public
            └── Tables
                 └── sensor_readings
</pre>

You can now inspect the table and execute SQL queries. <br>
Right click 'appdb' -> SQL editor -> open SQL script<br>

Example:
<pre>
CREATE TABLE IF NOT EXISTS sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(100) NOT NULL,
    measured_at TIMESTAMPTZ NOT NULL,
    temperature_c DOUBLE PRECISION,
    humidity_pct DOUBLE PRECISION,
    battery_pct DOUBLE PRECISION,
    created_at TIMESTAMPTZ not NULL DEFAULT NOW()
);


SELECT * FROM sensor_readings;

SELECT *
FROM sensor_readings
ORDER BY id DESC;

INSERT INTO sensor_readings (
    sensor_id,
    measured_at,
    temperature_c,
    humidity_pct,
    battery_pct
)
VALUES (
    'SENSOR_001',
    NOW(),
    23.5,
    65.2,
    87.0
);

</pre>

Highlight the code you want to run and press 'Ctrl+Enter' to run it <br>

## Testing the API Using Postman

The API is available at:
<pre>
  http://localhost:8080
</pre>

### Endpoint 1 – API health check

Method: GET

<pre>
GET http://localhost:8080/
</pre>

Expected response:
<pre>
{
    "message": "Sensor API is running"
}
</pre>

### Endpoint 2 – Create a sensor reading
Method: POST
In Postman, select Body → raw → JSON. <br>
example request:
<pre>
{
    "sensor_id": "sensor_001",
    "measured_at": "{{$isoTimestamp}}",
    "temperature_c": 22.5,
    "humidity_pct": 45.2,
    "battery_pct": 87.0
}
</pre>

<pre>
POST http://localhost:8080/readings
</pre>


Expected response (example):
<pre>
{
    "id": 1,
    "sensor_id": "sensor_001",
    "measured_at": "2026-11-10T09:30:00+00:00",
    "temperature_c": 22.5,
    "humidity_pct": 45.2,
    "battery_pct": 87.0
}
</pre>

The returned ID is generated automatically by PostgreSQL.

### Endpoint 3 – Get all sensor readings

Method: GET
<pre>
GET http://localhost:8080/readings
</pre>
Returns all stored sensor readings, ordered by measurement time, newest first.

### Endpoint 4 – Get the latest reading for each sensor

Method: GET
<pre>
GET http://localhost:8080/readings/latest
</pre>


## Project Overview

The environment consists of two Docker containers:

    PostgreSQL 18.6 – Database for storing sensor readings.
    FastAPI – Python-based REST API that communicates with PostgreSQL.

Two additional tools can be used to interact with the environment:

    DBeaver – Connect to PostgreSQL, inspect tables, and execute SQL queries.
    Postman – Send HTTP requests to the API and test its endpoints.
### Architecture
<pre>
                  ┌──────────────────┐
                  │     Postman      │
                  │   HTTP Requests  │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    FastAPI       │
                  │   sensor-api     │
                  │   Port: 8080     │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   PostgreSQL     │
                  │   postgres18     │
                  │   Port: 5432     │
                  └──────────────────┘
                           ▲
                           │
                  ┌────────┴─────────┐
                  │     DBeaver      │
                  │ Database Client  │
                  └──────────────────┘
</pre>

## Prerequisites

Install the following software before getting started:

    Docker Desktop or Docker Engine with Docker Compose.
    DBeaver Community Edition.
    Postman.

No local Python or PostgreSQL installation is required. Both are provided through Docker.
## Project Structure

The project should have the following directory structure:
<pre>
sensor-project/
│ 
├── docker-compose.yml
│
└── api/
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
</pre>






