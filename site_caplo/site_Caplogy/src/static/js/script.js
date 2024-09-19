
function redirectToPage(url) {
    window.location.href = url;
}

document.getElementById("calendrierButton").addEventListener("click", function() {
    window.location.href = "#calendrier";
});

//
document.addEventListener('DOMContentLoaded', function() {
        // Cache toutes les sections au chargement de la page
        var daySections = document.querySelectorAll('.day-section');
        daySections.forEach(function(section) {
            section.style.display = 'none';
        });

        // Ajoute un écouteur d'événements à chaque bouton
        var dayButtons = document.querySelectorAll('.day-button');
        dayButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                // Cache toutes les sections
                daySections.forEach(function(section) {
                    section.style.display = 'none';
                });

                // Affiche la section correspondant au bouton cliqué
                var target = button.getAttribute('data-target');
                document.getElementById(target).style.display = 'block';
            });
        });
    });


//pour calendrier
 document.addEventListener("DOMContentLoaded", function() {
        const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
        let currentYear = new Date().getFullYear();
        let currentMonth = new Date().getMonth();

        function generateCalendar(year, month) {
            const firstDay = new Date(year, month).getDay();
            const lastDate = new Date(year, month + 1, 0).getDate();
            let day = 1;
            const calendarBody = document.getElementById("calendarBody");
            calendarBody.innerHTML = "";
            document.getElementById("monthYear").innerHTML = `<strong>${monthNames[month]} ${year}</strong>`;

            for (let i = 0; i < 6; i++) {
                const row = document.createElement("tr");
                for (let j = 1; j <= 7; j++) {
                    const cell = document.createElement("td");
                    if ((i === 0 && j < firstDay) || day > lastDate) {
                        cell.innerHTML = "";
                    } else {
                        cell.innerHTML = day;
                        day++;
                    }
                    row.appendChild(cell);
                }
                calendarBody.appendChild(row);
                if (day > lastDate) break;
            }
        }

        document.getElementById("prevMonth").addEventListener("click", function() {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            generateCalendar(currentYear, currentMonth);
        });

        document.getElementById("nextMonth").addEventListener("click", function() {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            generateCalendar(currentYear, currentMonth);
        });

        generateCalendar(currentYear, currentMonth);
    });



document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menuPrincipale = document.getElementById('menu_principale');
    const closeMenu = document.getElementById('close-menu');

    menuToggle.addEventListener('click', function() {
        menuPrincipale.classList.toggle('show');
    });

    closeMenu.addEventListener('click', function() {
        menuPrincipale.classList.remove('show');
    });
});