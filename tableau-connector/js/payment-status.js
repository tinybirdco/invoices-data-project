(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "payment_range",
            alias: "Payment Range",
            dataType: tableau.dataTypeEnum.datetime
        }, {
            id: "pending",
            alias: "Pending (EUR)",
            dataType: tableau.dataTypeEnum.float
        }, {
            id: "payed",
            alias: "Payed (EUR)",
            dataType: tableau.dataTypeEnum.float
        }];

        var tableSchema = {
            id: "paymentstatus",
            alias: "Payment Status",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download the data
    myConnector.getData = function(table, doneCallback) {
        var dateObj = JSON.parse(tableau.connectionData),
            dateString = "start_date=" + dateObj.startDate + "&end_date=" + dateObj.endDate,
            apiCall = "https://api.tinybird.co/v0/pipes/dataflow__payments_status.json?" + dateString + "&token={TOKEN}"
        
        $.getJSON(apiCall, function(resp) {
            var feat = resp.data,
                tableData = [];

            // Iterate over the JSON object
            for (var i = 0, len = feat.length; i < len; i++) {
                tableData.push({
                    "payment_range": feat[i].payment_range,
                    "pending": feat[i].pending,
                    "payed": feat[i].payed
                });
            }

            table.appendRows(tableData);
            doneCallback();
        });
    };

    tableau.registerConnector(myConnector);

    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            var dateObj = {
                startDate: $('#start-date-one').val().trim(),
                endDate: $('#end-date-one').val().trim(),
            };

            // Simple date validation: Call the getDate function on the date object created
            function isValidDate(dateStr) {
                var d = new Date(dateStr);
                return !isNaN(d.getDate());
            }

            if (isValidDate(dateObj.startDate) && isValidDate(dateObj.endDate)) {
                tableau.connectionData = JSON.stringify(dateObj); // Use this variable to pass data to your getSchema and getData functions
                tableau.connectionName = "Payment Status"; // This will be the data source name in Tableau
                tableau.submit(); // This sends the connector object to Tableau
            } else {
                $('#errorMsg').html("Enter valid dates. For example, 2016-05-08.");
            }
        });
    });
})();
