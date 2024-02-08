#!/bin/bash
docker-compose down
docker rmi App
docker rmi BD
docker-compose up -d --build
docker image prune
docker builder prune