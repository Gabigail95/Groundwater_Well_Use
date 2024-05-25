document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display the first chart
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const ctx1 = document.getElementById('wellUseChart').getContext('2d');
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Well Use Count',
                        data: data.counts,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });

    const generateButton = document.getElementById('generateButton');
    generateButton.addEventListener('click', function() {
        const year1 = document.getElementById('year1').value;
        const year2 = document.getElementById('year2').value;

        fetch(`/second_chart_data?year1=${year1}&year2=${year2}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                const ctx2 = document.getElementById('averageGWEChart').getContext('2d');

                if (window.averageGWEChart instanceof Chart) {
                    window.averageGWEChart.destroy();
                }

                window.averageGWEChart = new Chart(ctx2, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: `Average GWE for ${year1}`,
                                data: data.avg_gwe_year1,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1
                            },
                            {
                                label: `Average GWE for ${year2}`,
                                data: data.avg_gwe_year2,
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                borderColor: 'rgba(153, 102, 255, 1)',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching second chart data:', error));
    });
});
