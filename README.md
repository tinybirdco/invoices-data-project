# Invoices data project

This data project demonstrates how [Tinybird](https://tinybird.co) could be used for real-time analytics retrieving data from BigQuery using the [CLI](https://docs.tinybird.co/cli.html) and [Apache Beam connector](https://pypi.org/project/tinybird-beam/).

This project is divided into:  
- **ds-gen**: Python script for generating the source dataset used to populate BigQuery
- **tb-project**: The Tinybird data project
- **tableau-connector**: The "connectors" to consume Tinybird APIs from Tableau

## Tableau Connector

Tableau does not provide out-of-the-box connectors for rest apis. In order to consume data from a rest API you should develop a specific connector ([WDC](https://tableau.github.io/webdataconnector/#)) which is basically a web page that executes the queries to the endpoint you want to consume. 

To be accessible from the Tableau server they can be deployed to a GCS bucket o any web server.
