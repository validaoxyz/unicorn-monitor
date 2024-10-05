#!/usr/bin/env python3

import time
import threading
import requests
import base64
import hashlib
from bech32 import bech32_encode, convertbits
from prometheus_client import start_http_server, Gauge

import os
import sys

# Configuration
CHAIN_ID = os.getenv('CHAIN_ID', 'unicorn-testnet')
VALOPER = os.getenv('VALOPER')
REST_ENDPOINT = os.getenv('REST_ENDPOINT', 'https://rest.testcorn-69.unicorn.meme')

# Metrics
MISSED_BLOCKS = Gauge('missed_blocks', 'Total number of missed blocks', ['chain_id'])
JAILED_STATUS = Gauge('jailed_status', 'Whether the validator is jailed, 1=jailed', ['chain_id'])
BONDING_STATUS = Gauge('bonding_status', 'If validator is active or not, 1=active', ['chain_id'])
BONDED_TOKENS = Gauge('bonded_tokens', 'The amount of coins staked to our validator', ['chain_id'])
DELEGATOR_COUNT = Gauge('delegator_count', 'The amount of individual wallets staked to our validator', ['chain_id'])

# Global variable for VALCONS
VALCONS = ''

def convert_pubkey(pubkey_json):
    # Extract the raw key from the JSON representation
    raw_pubkey = base64.b64decode(pubkey_json['key'])

    # Compute SHA256 hash of the public key
    sha256_hash = hashlib.sha256(raw_pubkey).digest()

    # Take the first 20 bytes of the SHA256 hash
    address_bytes = sha256_hash[:20]

    # Convert to 5-bit words for Bech32 encoding
    converted_bits = convertbits(address_bytes, 8, 5, pad=True)

    # Bech32-encode the address
    valcons_address = bech32_encode('unicornvalcons', converted_bits)

    return valcons_address

def get_validator_info():
    global VALCONS
    while True:
        try:
            # Get VALCONSPUB if not already obtained
            if not VALCONS:
                response = requests.get(f"{REST_ENDPOINT}/cosmos/staking/v1beta1/validators/{VALOPER}")
                response.raise_for_status()
                validator_info = response.json()
                VALCONSPUB = validator_info['validator']['consensus_pubkey']
                print(f"Consensus PubKey: {VALCONSPUB}")

                VALCONS = convert_pubkey(VALCONSPUB)
                print(f"VALCONS Address: {VALCONS}")

            # Collect metrics
            # Missed Blocks
            response = requests.get(f"{REST_ENDPOINT}/cosmos/slashing/v1beta1/signing_infos/{VALCONS}")
            response.raise_for_status()
            signing_info = response.json()
            missed_blocks = int(signing_info['val_signing_info']['missed_blocks_counter'])

            # Jailed Status
            jailed_status = validator_info['validator']['jailed']
            jailed_status = 1 if jailed_status == True else 0

            # Bonding Status
            bonding_status = validator_info['validator']['status']
            bonding_status = 1 if bonding_status == 'BOND_STATUS_BONDED' else 0

            # Bonded Tokens
            bonded_tokens = int(validator_info['validator']['tokens'])

            # Delegator Count
            response = requests.get(f"{REST_ENDPOINT}/cosmos/staking/v1beta1/validators/{VALOPER}/delegations")
            response.raise_for_status()
            delegations = response.json()
            delegator_count = int(delegations['pagination']['total'])

            # Update metrics with 'chain_id' label
            MISSED_BLOCKS.labels(chain_id=CHAIN_ID).set(missed_blocks)
            JAILED_STATUS.labels(chain_id=CHAIN_ID).set(jailed_status)
            BONDING_STATUS.labels(chain_id=CHAIN_ID).set(bonding_status)
            BONDED_TOKENS.labels(chain_id=CHAIN_ID).set(bonded_tokens)
            DELEGATOR_COUNT.labels(chain_id=CHAIN_ID).set(delegator_count)

            time.sleep(5)
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            time.sleep(5)

def main():
    # Start up the server to expose the metrics.
    start_http_server(9300)  # Port 9300 or any other unused port
    print("Starting exporter on port 9300")

    # Start the metrics collection in the background.
    metric_collector = threading.Thread(target=get_validator_info)
    metric_collector.daemon = True
    metric_collector.start()

    # Keep the main thread alive.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down exporter")
        sys.exit(0)

if __name__ == '__main__':
    main()
