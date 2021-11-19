#!/bin/bash

# wait for rabbitmq container
./docker/dev/wfi.sh -h rmq -p 5672 -t 60

python3 -m hwi