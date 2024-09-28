document.getElementById('extensionForm').addEventListener('submit', function(e) {
    console.log('FormS');
    e.preventDefault();
    const company = document.getElementById('textInput').value;
    const position = document.getElementById('dropdownSelect').value;
    const percent = document.getElementById('dropdownSelectPercent').value;
    
    fetch('http://0.0.0.0:10000/add_job_application', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            company: company,
            position: position,
            match: percent
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Job application added to Notion successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to add job application to Notion');
    });
});