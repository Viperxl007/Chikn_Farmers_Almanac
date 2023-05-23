# Chikn_Farmers_Almanac
This repo is a simple tool that calls the Chikn Farm API wallet summary and broadcasts the data locally to be scrapped by a prometheus instance in order to chart the status of your farm in Gragfana.  The scripts here are AS-IS there is no support. It will be periodically updated, feel free to contribute additional features.

# USING THIS SETUP
This is intended to be a self-hosted setup.  It assumes you know how to keep a python script running, run a Prometheus instance and setup grafana to read the Prometheus database.

The files herein can be dropped into such a setup but nothing here is intended to teach you about those 3 pieces of the tool.

If you don't know how to do these things, I hear chatGPT is pretty capable these days ;-)

# Contributions must preserve original functionality
Any contributions made must preserve original functionality.

Steps to run:
- Run the Chikn_Farm_Extractor script which is hard coded to call the wallet summary API every 180 seconds.  Pass the wallet address you wish to monitor as a param:

Example:
chikn_farm_exporter.py 0x123456789

- Either use the Prometheus .yml config file or copy the extractor job into your existing Prometheus .yml

- Setup the prometheus data source in Grafana and import the dashboard JSON file or start creating your own dashboard pulling from the Prometheus time series database.

BOK BOK
