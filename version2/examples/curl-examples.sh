#!/bin/sh

curl http://127.0.0.1:5000/registers
curl http://127.0.0.1:5000/registers/TEMP_EXT

# POST Data
curl http://127.0.0.1:5000/registers/TEMP_ECS -H 'Content-Type: application/json' -X POST -d '{ \"TEMP_ECS\": [ 45.0 ] }'
