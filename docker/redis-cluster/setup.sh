#!/bin/bash

docker volume rm -f $(docker volume ls --filter "name=redis-cluster") &&

docker-compose up -d
sleep 4

docker exec -it redis-cluster-redis-1-1 redis-cli --cluster create 172.38.0.11:6379 172.38.0.12:6379 172.38.0.13:6379 172.38.0.14:6379 172.38.0.15:6379 172.38.0.16:6379 --cluster-replicas 1 &&

echo "finished. connection IP is 127.0.0.1:6371. Connect with 'redis-cli -c -p 6371'. test with 'CLUSTER NODES'"