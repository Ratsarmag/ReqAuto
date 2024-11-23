document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('data-container');
            data.forEach(item => {
                const div = document.createElement('div');
                div.textContent = JSON.stringify(item);
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Error:', error));
});