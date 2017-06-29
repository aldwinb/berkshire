#!/usr/bin/env bash

if [ -n "$STDIN_OPEN" ]; then
  docker-compose up --build -d
  docker exec -it berkshire-1 bash
else
  docker-compose up --build
fi