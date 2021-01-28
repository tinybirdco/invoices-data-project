(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "recipient_code",
            alias: "Recipient Code",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "country",
            alias: "Country",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "total",
            alias: "Total (EUR)",
            dataType: tableau.dataTypeEnum.float
        }];

        var tableSchema = {
            id: "toprecipientsfeed",
            alias: "Top 10 Recipients (Ranking)",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download the data
    myConnector.getData = function(table, doneCallback) {
        var apiCall = "https://api.tinybird.co/v0/pipes/dataflow__top_recipients.json?toktoken={TOKEN}"
        
        $.getJSON(apiCall, function(resp) {
            var feat = resp.data,
                tableData = [];

            // Iterate over the JSON object
            for (var i = 0, len = feat.length; i < len; i++) {
                tableData.push({
                    "recipient_code": feat[i].recipient_code,
                    "country": feat[i].country,
                    "total": feat[i].total
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
            tableau.connectionName = "Top 10 Recipients"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();
