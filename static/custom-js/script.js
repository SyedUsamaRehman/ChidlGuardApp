// Sample accelerometer data (replace with your actual data)
const accelerometerData = [
    // Your accelerometer data here
];

// Function to filter data based on selected interval
function filterDataByInterval(interval) {
    const now = new Date();
    let filterFunction;

    switch (interval) {
        case 'daily':
            filterFunction = entry => {
                const entryDate = new Date(entry.Timestamp);
                return entryDate.toDateString() === now.toDateString();
            };
            break;
        case 'weekly':
            filterFunction = entry => {
                const entryDate = new Date(entry.Timestamp);
                const weekAgo = new Date(now);
                weekAgo.setDate(now.getDate() - 7);
                return entryDate >= weekAgo;
            };
            break;
        case 'monthly':
            filterFunction = entry => {
                const entryDate = new Date(entry.Timestamp);
                return entryDate.getMonth() === now.getMonth();
            };
            break;
        default:
            filterFunction = () => true; // Default to show all data
            break;
    }

    return accelerometerData.filter(filterFunction);
}

// Function to update the chart
function updateChart(interval) {
    const filteredData = filterDataByInterval(interval);

    // Extract timestamps and data values for each axis
    const timestamps = filteredData.map(entry => entry.Timestamp);
    const xAxisData = filteredData.map(entry => parseFloat(entry['X-axis (m/s^2)']));
    const yAxisData = filteredData.map(entry => parseFloat(entry['Y-axis (m/s^2)']));
    const zAxisData = filteredData.map(entry => parseFloat(entry['Z-axis (m/s^2)']));

    // Get the canvas element
    const ctx = document.getElementById('accelChart').getContext('2d');

    // Clear existing chart if exists
    if (window.accelChart) {
        window.accelChart.destroy();
    }

    // Create the new chart
    window.accelChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: 'X-axis',
                    borderColor: 'rgb(255, 99, 132)',
                    data: xAxisData,
                    fill: false
                },
                {
                    label: 'Y-axis',
                    borderColor: 'rgb(54, 162, 235)',
                    data: yAxisData,
                    fill: false
                },
                {
                    label: 'Z-axis',
                    borderColor: 'rgb(75, 192, 192)',
                    data: zAxisData,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `Accelerometer Data (${interval.charAt(0).toUpperCase() + interval.slice(1)})`
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Timestamp'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Acceleration (m/s^2)'
                    }
                }
            }
        }
    });
}

// Initial chart update based on default selection
updateChart('daily');

// Event listener for select change
const intervalSelect = document.getElementById('intervalSelect');
intervalSelect.addEventListener('change', function() {
    const selectedInterval = this.value;
    updateChart(selectedInterval);
});
