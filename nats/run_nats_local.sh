#!/usr/bin/bash
docker run --rm --name nats-srv -p 4222:4222 nats:linux -DV
