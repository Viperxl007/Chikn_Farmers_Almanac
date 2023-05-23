# Chikn_Farmers_Almanac
This repo is a simple tool that calls the Chikn Farm API wallet summary and broadcasts the data locally to be scrapped by a prometheus instance in order to chart the status of your farm in Gragfana.  The scripts here are AS-IS there is no support. It will be periodically updated, feel free to contribute additional features.

# Contributions must preserve original functionality
Any contributions made must preserve original functionality.

Steps to run:
- Run the Chikn_Farm_Extractor script which is hard coded to call the wallet summary API every 180 seconds.  Pass the wallet address you wish to monitor as a param:

Example:
chikn_farm_extractor.py 0x123456789

- Either use the Prometheus .yml config file or copy the extractor job into your existing Prometheus .yml

- Setup the prometheus data source in Grafana and import the dashboard JSON file or start creating your own dashboard pulling from the Prometheus time series database.

BOK BOK
