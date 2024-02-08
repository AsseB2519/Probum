#!/bin/bash
docker-compose down --rmi all --remove-orphans
docker-compose up -d --build
docker builder prune  -a -f