const formIds = ['studentQuery', 'orderUpload', 'flashUpload', 'panelQuery', 'mixedQuery']

function hideAllForms(){
    for(let formId of formIds){
        document.getElementById(formId).style.display = 'none';
    }
}
function onlyKeepForm(id){
    hideAllForms();
    hideTable()
    document.getElementById(id).style.display = 'block';
}

function hideTable(){
    const table = document.getElementById('dataTable');
    table.style.display = 'none';
}
function unhideTable(){
    const table = document.getElementById('dataTable');
    table.style.display = 'block';
}


function emptyTable(){
    const table = document.getElementById('dataTable');

    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
}
function displayData(data) {
    const table = document.getElementById('dataTable');
    emptyTable();

    if(!data || !data.length){
        const row = table.insertRow();
        const cellHeader = row.insertCell();
        cellHeader.textContent = "Nothing found";
        cellHeader.style.fontWeight = 'bold';
    } else {
        for (let property in data[0]) {
            if (data[0].hasOwnProperty(property)) {
                const row = table.insertRow();
                const cellHeader = row.insertCell();
                cellHeader.textContent = property;
                cellHeader.style.fontWeight = 'bold';

                data.forEach(function(item) {
                    const cell = row.insertCell();
                    cell.textContent = item[property];
                });
            }
        }
    }
    unhideTable();
}