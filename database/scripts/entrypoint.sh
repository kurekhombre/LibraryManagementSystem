#!/bin/bash
psql -h localhost -p 5432 -U library -d library -f /usr/src/app/101_create_tables.sql
psql -h localhost -p 5432 -U library -d library -f /usr/src/app/102_insert_data.sql