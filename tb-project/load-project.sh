#!/bin/bash 

# This script automatically creates the TB project. You need to have installed and authenticated 
# our TB CLI. 
# Resources are created in the account you are currently logged in.
# You need source datasets for loading data. You can find them using:
#   gsutil cp -r gs://poc-invoices/* .
#


check_response() {

    if [ $1 -eq 0 ]
    then
        echo $2
    else
        echo $3
        exit -1
    fi
}

create() {
    ## Create datasources
    for filename in datasources/*.datasource; do
        echo "Creating: $filename"
        tb push $filename --prefix $1
        ret=$?
        check_response $ret "Sucess: $filename" "Error: $filename"
    done

    ## Create pipes
    for filename in pipes/*.pipe; do
        echo "Creating: $filename"
        tb push $filename --prefix $1
        ret=$?
        check_response $ret "Sucess: $filename" "Error: $filename"
    done

    ## Create endpoints
    for filename in endpoints/*.pipe; do
        echo "Creating: $filename"
        tb push $filename --prefix $1
        ret=$?
        check_response $ret "Sucess: $filename" "Error: $filename"
    done

    echo "Loading clients ..."
    tb datasource append $1"__clients" ../../datasets/bq/clients.csv
    ret=$?
    check_response $ret "Uploaded clients" "Error uploading clients"

    echo "Loading recipients ..."
    tb datasource append $1"__recipients" ../../datasets/bq/recipients.csv
    ret=$?
    check_response $ret "Uploaded recipients" "Error uploading recipients"

    echo "Loading currency"
    tb datasource append $1"__currency" ../../datasets/currency/currencies.csv
    ret=$?
    check_response $ret "Uploaded currencies" "Error uploading currencies"

    echo "Loading invoices ..."
    ./upload-invoices.sh ../../datasets/bq/invoices/invoices $1
    ret=$?
    check_response $ret "Uploaded invoices" "Error uploading invoices"

}

delete() {

    ## delete datasources
    for filename in datasources/*.datasource; do
        ds=`echo "$filename" | sed -r "s/.+\/(.+)\..+/\1/"`
        echo "Deleting: $ds"
        tb datasource rm $1__$ds
        ret=$?
        check_response $ret "Deleted: $filename" "Error deleting: $filename"
    done

    ## delete pipes
    for filename in pipes/*.pipe; do
    p=`echo "$filename" | sed -r "s/.+\/(.+)\..+/\1/"`
    echo "Deleting: $p"
    tb pipe rm $1__$p
    ret=$?
    check_response $ret "Sucess: $filename" "Error: $filename"
    done

    ## delete endpoints
    for filename in endpoints/*.pipe; do
    ep=`echo "$filename" | sed -r "s/.+\/(.+)\..+/\1/"`
    echo "Deleting: $ep"
    tb pipe rm $1__$ep
    ret=$?
    check_response $ret "Sucess: $filename" "Error: $filename"
    done

}

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <create|delete> <prefix for creating|deleting TB resources>"
    exit -1
fi

case $1 in

  "create")
    create $2
    ;;

  "delete")
    delete $2
    ;;
esac
