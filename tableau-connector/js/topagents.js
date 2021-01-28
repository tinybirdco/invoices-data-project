(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "position",
            alias: "Position",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "agent_id",
            alias: "Agente",
            dataType: tableau.dataTypeEnum.int
        }, {
            id: "total",
            alias: "Total (EUR)",
            dataType: tableau.dataTypeEnum.float
        }];

        var tableSchema = {
            id: "topagentsfeed",
            alias: "Top 10 Agents (Ranking)",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download the data
    myConnector.getData = function(table, doneCallback) {
        var apiCall = "https://api.tinybird.co/v0/pipes/dataflow__top_agents.json?token={TOKEN}"
        
        $.getJSON(apiCall, function(resp) {
            var feat = resp.data,
                tableData = [];

            // Iterate over the JSON object
            for (var i = 0, len = feat.length; i < len; i++) {
                tableData.push({
                    "position": feat[i].position,
                    "agent_id": feat[i].agent_id,
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
            tableau.connectionName = "Top 10 Agents"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();
