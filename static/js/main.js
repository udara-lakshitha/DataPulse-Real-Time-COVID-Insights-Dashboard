const countrySelect = document.getElementById('country-select');
const periodSelect = document.getElementById('period-select');
const loader = document.getElementById('loader');
const plotImg = document.getElementById('covid-plot');

const statDate = document.getElementById('stat-date');
const statTotalCases = document.getElementById('stat-total-cases');
const statNewCases = document.getElementById('stat-new-cases');
const statTotalVaccinations = document.getElementById('stat-total-vaccinations');
const statPeopleVaccinated = document.getElementById('stat-people-vaccinated');

async function updateData() {
    loader.style.display = 'block';
    plotImg.style.display = 'none';

    const country = countrySelect.value;
    const period = periodSelect.value;

    try {
        const response = await fetch('/update_data', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({country, period})
        });

        if (!response.ok) {
            throw new Error('Network error');
        }

        const data = await response.json();

        plotImg.src = data.plot_url;
        plotImg.onload = () => {
            loader.style.display = 'none';
            plotImg.style.display = 'block';
        };

        statDate.textContent = data.stats.date;
        statTotalCases.textContent = data.stats.total_cases;
        statNewCases.textContent = data.stats.new_cases;
        statTotalVaccinations.textContent = data.stats.total_vaccinations;
        statPeopleVaccinated.textContent = data.stats.people_vaccinated_per_hundred;
    } catch (error) {
        loader.style.display = 'none';
        plotImg.style.display = 'block';
        alert('Failed to update data: ' + error.message);
    }
}

countrySelect.addEventListener('change', updateData);
periodSelect.addEventListener('change', updateData);

// Auto refresh every 6 hours (21600000 ms)
setInterval(updateData, 21600000);