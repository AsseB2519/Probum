#!/bin/bash
docker-compose down --rmi all --remove-orphans
docker builder prune -a -f