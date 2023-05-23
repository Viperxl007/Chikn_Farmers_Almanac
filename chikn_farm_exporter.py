import argparse
import re
from prometheus_client import start_http_server, Gauge
import requests
import time

# Initialize an empty dictionary to hold our Gauges
GAUGES = {}

#define a gauge metric
WALLET_SUMMARY = Gauge('chikn_farm_wallet_summary', 'Wallet summary from Chikn Farm', ['metrics'])

# Define separate gauge metrics for eggReport and feedReport
EGG_REPORT_METRICS = {}
FEED_REPORT_METRICS = {}

def sanitize_label_name(name):
    """Sanitize label names to conform with Prometheus label naming ruls."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def fetch_data(wallet_address):
    while True:
        # Fetch the data from the API
        response = requests.get(f'https://api.chikn.farm/api/wallet/{wallet_address}/summary')

        # Check if the request was successful
        if response.status_code == 200:
            print(f'Successfully fetched data for wallet: {wallet_address}')
            data = response.json()

            # Process eggReport and feedReport separately
            for report_name in ['eggReport', 'feedReport']:
                if report_name in data:
                    for sub_key, sub_value in data[report_name].items():
                        # Only process if sub_value is a number and key is not 'lastClaimedTs'
                        if isinstance(sub_value, (int,float)) and sub_key != 'lastClaimedTs':
                            # Create a new gauge metric if it doesn't exist
                            gauge_key = f'chikn_farm_{report_name}_{sub_key}'
                            if gauge_key not in GAUGES:
                                GAUGES[gauge_key] = Gauge(gauge_key, f'{report_name} {sub_key} from Chikn Farm')
                            # Set the metric value
                            GAUGES[gauge_key].set(sub_value)
                    del data[report_name] # remove the key from the data dict after processing

            # Handle weightDistribution and rarirityDistribution by summing values
            for key in ['weightDistribution', 'rarityDistribution']:
                print(f'INFO: Deleting: {key}')
                if key in data:
                    del data[key]

            # Now process the remaining top level keys
            for key, value in data.items():
                if isinstance(value, (int, float)):
                    print(f'INFO: processing: {key} with a value of: {value}')
                    sanitized_key = sanitize_label_name(f'chikn_farm_{key}')
                    # Create a new gauge metric if it doesn't exist
                    if sanitized_key not in GAUGES:
                        GAUGES[sanitized_key] = Gauge(sanitized_key, f'{key} from Chikn Farm')
                    #set the metric value
                    GAUGES[sanitized_key].set(value)

                    #print(f'Setting value for label: {sanitized_key} with a value of: {value}')
                    #WALLET_SUMMARY.labels(metric=sanitized_key).set(value)

        else:
            print(f'Failed to fetch data for wallet: {wallet_address}. Response status code: {response.status_code}')

        # Sleep for 3 minutes (180 seconds) before fetching the data again
        print(f'................ WAITING ..............')
        print(f'.......................................')
        print(f'.......................................')
        time.sleep(180)

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('wallet_address', help='Wallet address to fetch data for')
    args = parser.parse_args()

    # Start up the server to expose the metrics.
    start_http_server(8000)
    fetch_data(args.wallet_address)

