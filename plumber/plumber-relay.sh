#!/bin/bash
#
# Simple start script
#
PLUMBER_RELAY_TYPE=rabbit \
PLUMBER_RELAY_TOKEN=Changeme\
PLUMBER_RELAY_GRPC_ADDRESS=grpc-collector.batch.sh:9000 \
PLUMBER_RELAY_RABBIT_ADDRESS=amqp://guest:guest@localhost \
PLUMBER_RELAY_RABBIT_EXCHANGE=event \
PLUMBER_RELAY_RABBIT_QUEUE=plumber \
PLUMBER_RELAY_RABBIT_ROUTING_KEY="messages.billing.create_account" \
plumber relay --listen-address=":8081" --stats --skip-verify-tls
