#!/bin/bash
#
# Simple start script
#
PLUMBER_RELAY_TYPE=rabbit \
PLUMBER_RELAY_TOKEN=changeme \
PLUMBER_RELAY_GRPC_ADDRESS=grpc-collector.batch.sh:9000 \
PLUMBER_RELAY_RABBIT_ADDRESS=amqp://guest:guest@localhost \
PLUMBER_RELA:Y_KAFKA_TOPIC=rsvps \
PLUMBER_RELAY_KAFKA_GROUP_ID=BatchRelay \
PLUMBER_RELAY_KAFKA_USE_CONSUMER_GROUP=true \
plumber relay --listen-address=":8081" --stats
