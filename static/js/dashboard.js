/* Dashboard JavaScript */

let threatsChart = null;
let severityChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
    loadThreatsChart();
    loadSeverityChart();
    loadRecentThreats();
    // Refresh every 30 seconds
    setInterval(refreshData, 30000);
});

function refreshData() {
    loadDashboardStats();
    loadThreatsChart();
    loadRecentThreats();
}

function loadDashboardStats() {
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-events').textContent = data.total_events.toLocaleString();
            document.getElementById('threats-detected').textContent = data.threats_detected.toLocaleString();
            document.getElementById('critical-alerts').textContent = data.critical_alerts.toLocaleString();
            document.getElementById('incidents').textContent = data.incidents.toLocaleString();
            document.getElementById('blocked-events').textContent = data.blocked_events.toLocaleString();
            document.getElementById('system-health').textContent = data.system_health.toFixed(1) + '%';
        })
        .catch(error => console.error('Error loading dashboard stats:', error));
}

function loadThreatsChart() {
    fetch('/api/dashboard/threats-timeline')
        .then(response => response.json())
        .then(data => {
            const labels = data.map(d => d.time);
            const totals = data.map(d => d.total_events);
            const suspicious = data.map(d => d.suspicious_events);

            const ctx = document.getElementById('threatsChart');
            
            if (threatsChart) {
                threatsChart.destroy();
            }

            threatsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Total Events',
                            data: totals,
                            borderColor: '#00d4ff',
                            backgroundColor: 'rgba(0, 212, 255, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Suspicious Events',
                            data: suspicious,
                            borderColor: '#ff3333',
                            backgroundColor: 'rgba(255, 51, 51, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#e0e0e0',
                                font: { size: 12 }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#a0a0a0' }
                        },
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { color: '#a0a0a0' }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading threats chart:', error));
}

function loadSeverityChart() {
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            const severityData = data.severity_distribution;
            const labels = severityData.map(s => s.severity.charAt(0).toUpperCase() + s.severity.slice(1));
            const counts = severityData.map(s => s.count);
            const colors = {
                'Critical': '#ff3333',
                'High': '#ffaa00',
                'Medium': '#ffdd00',
                'Low': '#00ff88'
            };
            const backgroundColor = labels.map(l => colors[l] || '#6c757d');

            const ctx = document.getElementById('severityChart');
            
            if (severityChart) {
                severityChart.destroy();
            }

            severityChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: counts,
                        backgroundColor: backgroundColor,
                        borderColor: 'rgba(0, 0, 0, 0.3)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#e0e0e0',
                                font: { size: 11 }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading severity chart:', error));
}

function loadRecentThreats() {
    fetch('/api/alerts?per_page=5')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('threats-table');
            tbody.innerHTML = '';
            
            if (data.alerts.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-secondary py-3">No threats detected</td></tr>';
                return;
            }
            
            data.alerts.forEach(alert => {
                const timestamp = new Date(alert.timestamp).toLocaleString();
                const severityClass = `severity-${alert.severity}`;
                const statusClass = `status-${alert.status}`;
                
                const row = `
                    <tr>
                        <td><small>${timestamp}</small></td>
                        <td><code>${alert.source_ip}</code></td>
                        <td>
                            <span class="threat-indicator ${alert.severity}"></span>
                            ${alert.threat_type}
                        </td>
                        <td>
                            <strong>${alert.risk_score.toFixed(1)}</strong>
                            <div class="progress" style="height: 4px; margin-top: 4px;">
                                <div class="progress-bar" style="width: ${alert.risk_score}%; background-color: ${getSeverityColor(alert.severity)};"></div>
                            </div>
                        </td>
                        <td><span class="alert-badge ${alert.severity}">${alert.severity.toUpperCase()}</span></td>
                        <td><span class="status-pill ${alert.status}">${alert.status.charAt(0).toUpperCase() + alert.status.slice(1)}</span></td>
                    </tr>
                `;
                tbody.innerHTML += row;
            });
        })
        .catch(error => console.error('Error loading recent threats:', error));
}

function getSeverityColor(severity) {
    const colors = {
        'critical': '#ff3333',
        'high': '#ffaa00',
        'medium': '#ffdd00',
        'low': '#00ff88'
    };
    return colors[severity] || '#6c757d';
}
