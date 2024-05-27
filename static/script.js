document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('creatureForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
        jsonData['is_player'] = formData.get('is_player') === 'on';

        fetch('/add_creature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        })
        .then(response => response.json())
        .then(data => {
            if (! data.success) {
                alert('Error adding creature.');
            }
            form.reset();
            loadCreatures();
        });
    });

    document.getElementById('removePlayersButton').addEventListener('click', function(e) {
        e.preventDefault();
        removePlayers();
    });

    document.getElementById('creaturesTable').addEventListener('click', function(event) {
        if (event.target.classList.contains('delete')) {
            const row = event.target.closest('tr');
            const creatureId = row.getAttribute('data-id');
            
            fetch('/remove_selected', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: creatureId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.remove();
                } else {
                    alert('Failed to delete creature');
                }
            });
        }

        if (event.target.classList.contains('update')) {
            const row = event.target.closest('tr');
            const id = row.getAttribute('data-id');
            const health = row.cells[3].innerText;
            const armorClass = row.cells[4].innerText;

            const jsonData = { id, health, armorClass };

            fetch('/update_character', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData),
            })
            .then(response => response.json())
            .then(data => {
                if (! data.success) {
                    alert('Error updating creature.');
                }
                loadCreatures()
            });
        }
    });

    function loadCreatures() {
        fetch('/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const tbody = doc.querySelector('#creaturesTable tbody');
                document.querySelector('#creaturesTable tbody').innerHTML = tbody.innerHTML;
            });
    }

    function removePlayers() {
        fetch('/remove_players', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(result => {
            if (! result.success) {
                alert(result.message);
            }
        });
        loadCreatures();
    }
    

    loadCreatures();
});
