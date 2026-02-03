#!/usr/bin/env bash
# Feature: test command examples — quick CURL commands to exercise the API. Connects: tests and local server.
##################### API Observation Via Codespace URL
##################### API Observation Via Hopscotch
##################### API Observation Via CURL

# A. Get All Patients
curl -X GET "https://potential-space-garbanzo-9vvgrgg65j6cj5v-8000.app.github.dev/api/patients"

# B. Get One Patient
curl -X GET "http://localhost:8000/api/patients/1"

# C. Create Patient
curl -X POST "http://localhost:8000/api/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson",
    "dob": "1990-01-01",
    "phone": "555-1212",
    "email": "alice@example.com",
    "address": "123 Main St"
  }'

# D. Update Patient
curl -X PUT "http://localhost:8000/api/patients/1" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice Updated",
    "last_name": "Johnson",
    "dob": "1990-01-01",
    "phone": "555-9999",
    "email": "alice_new@example.com",
    "address": "456 Market St"
  }'

# E. Delete Patient
curl -X DELETE "http://localhost:8000/api/patients/1"


##################### DB Observation Via SQLite Web
- install https://github.com/coleifer/sqlite-web
- pip install sqlite-web
- sqlite_web students.db