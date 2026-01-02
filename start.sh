#!/bin/bash
cd "$(dirname "$0")"

sudo docker compose -f jupyter_docker-compose.yml up -d

sleep 3

firefox -new-tab "http://localhost:8765/lab?"
