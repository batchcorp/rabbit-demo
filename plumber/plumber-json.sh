#!/bin/bash
plumber read kafka --topic hello --address="ec2-3-139-154-3.us-east-2.compute.amazonaws.com:9092" --follow --json
