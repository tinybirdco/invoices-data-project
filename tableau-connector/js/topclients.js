(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "company_name",
            alias: "Company Name",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "company_country",
            alias: "Company Country",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "total",
            alias: "Total (EUR)",
            dataType: tableau.dataTypeEnum.float
        }];

        var tableSchema = {
            id: "topclientsfeed",
            alias: "Top 10 Clients (Ranking)",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download the data
    myConnector.getData = function(table, doneCallback) {
        var apiCall = "https://api.tinybird.co/v0/pipes/dataflow__top_clients.json?token={TOKEN}"
        
        $.getJSON(apiCall, function(resp) {
            var feat = resp.data,
                tableData = [];

            // Iterate over the JSON object
            for (var i = 0, len = feat.length; i < len; i++) {
                tableData.push({
                    "company_name": feat[i].company_name,
                    "company_country": feat[i].company_country,
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
            tableau.connectionName = "Top 10 Clients"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();
