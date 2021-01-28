#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: upload-invoices.sh <invoices path to csv files> <prefix>"
    exit -1
fi

for filename in $1/*; do
   echo "Uploading file: $filename"
   tb datasource append $2__invoices $filename
done

