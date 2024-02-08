function uploadOrdersFile() {
    const formData = new FormData();
    const file = document.getElementById('ordersFileInput').files[0];
    formData.append('file', file);
    fetch('/upload_orders/', {
        method: 'POST',
        body: formData
    });
    window.location.reload();
}
function uploadFlashFile() {
    const formData = new FormData();
    const file = document.getElementById('flashFileInput').files[0];
    formData.append('file', file);
    fetch('/upload_flash/', {
        method: 'POST',
        body: formData
    });
    window.location.reload();
}
function submitStudentForm() {
    const name = document.getElementById('studentSearchInput').value;
    if (name.trim() !== '') {
        fetch(`/students/${name}`)
        .then(response => response.json())
        .then(data => {
            displayData(data);
        })
        .catch(error => console.error('Error:', error));
    }
}

function submitPanelForm() {
        const panel = document.getElementById('panelSearchInput').value;
        if (panel.trim() !== '') {
            fetch(`/panels/${panel}`)
            .then(response => response.json())
            .then(data => {
              displayData(data);
            })
            .catch(error => console.error('Error:', error));
        }
}

function submitMixedForm() {
    const query = document.getElementById('mixedSearchInput').value;
    if (query.trim() !== '') {
        fetch(`/mixed/${query}`)
        .then(response => response.json())
        .then(data => {
            displayData(data);
        })
        .catch(error => console.error('Error:', error));
    }
}

function downloadStudent() {
    const name = document.getElementById('studentSearchInput').value;
    if (name.trim() !== '') {
        window.open(`/students/${name}/download`)
    }
}
function downloadPanel() {
    const panel = document.getElementById('panelSearchInput').value;
    if (panel.trim() !== '') {
        window.open(`/panels/${panel}/download`)
    }
}
function downloadMixed() {
    const query = document.getElementById('mixedSearchInput').value;
    if (query.trim() !== '') {
        window.open(`/mixed/${query}/download`)
    }
}