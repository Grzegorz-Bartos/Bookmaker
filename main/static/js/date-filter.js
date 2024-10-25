document.getElementById('date-filter').addEventListener('change', function() {
    const selectedDate = this.value;
    const matchRows = document.querySelectorAll('#matches-table tr');

    matchRows.forEach(row => {
        const matchDate = row.getAttribute('data-date');
        if (selectedDate === 'all' || matchDate === selectedDate) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});