#!/bin/bash

# wait for rabbitmq container
./docker/prod/wfi.sh -h rmq -p 5672

python3 -m hwi