$(document).ready(function() {
    $("#downloadBtn").hide();

    $("#inputCols").keydown(function(event) {
        // generate csv from columns given
        if (event.key == "Enter") {
            let columns = $("#inputCols").val();
            
            
            console.log("input: "+columns);
            
            // create table head
            let headHTML = parseTable(columns, "th");
            $("table").html(headHTML);

            // request table rows from server
            console.log(columns);

            // show loader in middle of table
            $("#loader").css({"visibility": "visible", "display": "block"});

            // generate table then hide loader and show download button
            generate_table(columns, 10);
        }
    });

    $("#downloadBtn").click(function() {
        console.log("download button clicked")
        const tableHTML = `<table>${$("table").html()}</table>`;
        $.ajax({
            type: "POST",
            url: "/save_table",
            data: {"table": tableHTML},
            success: function(data) {
                let url = window.URL.createObjectURL(new Blob([data]));
                let a = document.createElement('a');
                a.href = url;
                a.download = "fake_table.csv";
                document.body.append(a);
                a.click();
                a.remove();
            },
            error: function(data) {
                console.log("Download failed");
            }
        });

    })
});

function generate_table(columns, nrows=10) {
    $.ajax({
        type: "POST",
        url: "/generate_table",
        data: {"columns": columns, "nrows": nrows},
        success: function(data) {
            let rows = data.split("\n\n");
            rows.forEach(row => {
                row = row.trim();
                if (row != "") {
                    row = JSON.parse(row).text;
                    let dataHTML = parseTable(row, "td");
                    $("table").append(dataHTML);
                }
            });
            $("#loader").fadeOut(500);

            // after all rows generated, fade in download button
            $("#downloadBtn").fadeIn(1000);
        },
        error: function(response) {
            console.log("Data generation failed");
        }
    });
}

function parseTable(inputText="", tag="td") {
    let cols = inputText.split(",");
    let rowHTML = "<tr>"
    cols.forEach(col => {
        col = col.trim();
        if (col != ""){
            let row = `<${tag}>${col}</${tag}>`
            rowHTML += row;
        }
    })
    rowHTML += `</tr>`
    return rowHTML;
}