#!/bin/bash
docker-compose down
docker rmi APIAutenticacao
docker rmi APIDados
docker rmi WebSite
docker image prune
docker builder prune