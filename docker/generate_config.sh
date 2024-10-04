#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

# Substitute variables in prometheus.yml.tmpl and save as prometheus.yml
envsubst < ../prometheus/prometheus.yml.tmpl > ../prometheus/prometheus.yml
