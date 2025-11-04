// Gráficos e funcionalidades do dashboard
class DashboardCharts {
    constructor() {
        this.currentStationId = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initCharts();
    }

    setupEventListeners() {
        // Event listener para seleção de estação
        document.getElementById('station-select').addEventListener('change', (e) => {
            this.currentStationId = e.target.value;
            if (this.currentStationId) {
                this.loadStationData(this.currentStationId);
            } else {
                this.clearCharts();
            }
        });
    }

    initCharts() {
        // Gráfico das últimas 24 horas
        const ctx24h = document.getElementById('grafico-24h').getContext('2d');
        this.charts.grafico24h = new Chart(ctx24h, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'PM2.5',
                        data: [],
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'PM10',
                        data: [],
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'NO₂',
                        data: [],
                        borderColor: '#F39E56',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'O³',
                        data: [],
                        borderColor: '#c567CE56',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'SO²',
                        data: [],
                        borderColor: '#FCC756',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'CO',
                        data: [],
                        borderColor: '#CC0406',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Variação dos Poluentes (24h)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'µg/m³'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Horário'
                        }
                    }
                }
            }
        });

        // Gráfico dos últimos 7 dias
        const ctx7d = document.getElementById('grafico-7dias').getContext('2d');
        this.charts.grafico7dias = new Chart(ctx7d, {
            type: 'line',
            //data: {
            //    labels: [],
            //    datasets: [
            //        {
            //            label: 'AQI Médio',
            //            data: [],
            //            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            //            borderColor: 'rgba(75, 192, 192, 1)',
            //            borderWidth: 1,
            //            type: 'line',
            //            fill: false,
            //            tension: 0.4,
            //            yAxisID: 'y'
            //        },
            //        {
            //            label: 'PM2.5',
            //            data: [],
            //            backgroundColor: 'rgba(255, 99, 132, 0.6)',
            //            borderColor: 'rgba(255, 99, 132, 1)',
            //            borderWidth: 1,
            //            yAxisID: 'y1'
            //        }
            //    ]
            //},

            //! DADOS
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'PM2.5',
                        data: [],
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'PM10',
                        data: [],
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'NO₂',
                        data: [],
                        borderColor: '#F39E56',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'O³',
                        data: [],
                        borderColor: '#c567CE56',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'SO²',
                        data: [],
                        borderColor: '#FCC756',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'CO',
                        data: [],
                        borderColor: '#CC0406',
                        backgroundColor: 'rgba(255, 206, 86, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                ]
            },
            //options: {
            //    responsive: true,
            //    maintainAspectRatio: false,
            //    plugins: {
            //        title: {
            //            display: true,
            //            text: 'Tendência Semanal'
            //        }
            //    },
            //    scales: {
            //        y: {
            //            type: 'linear',
            //            display: true,
            //            position: 'left',
            //            title: {
            //                display: true,
            //                text: 'AQI'
            //            }
            //        },
            //        y1: {
            //            type: 'linear',
            //            display: true,
            //            position: 'right',
            //            title: {
            //                display: true,
            //                text: 'PM2.5 (µg/m³)'
            //            },
            //            grid: {
            //                drawOnChartArea: false
            //            }
            //        },
            //        x: {
            //            title: {
            //                display: true,
            //                text: 'Data'
            //            }
            //        }
            //    }
            //}
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Variação dos Poluentes 7 dias'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'µg/m³'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Dias'
                        }
                    }
                }
            }
        });
    }

    async loadStationData(stationId) {
        try {
            // Carrega dados dos últimos 7 dias
            const response = await fetch(`/api/estacao/${stationId}/`);
            const data = await response.json();
            
            if (data.success) {
                this.updateCurrentIndicators(data.dados);
                this.update24hChart(data.dados);
                this.update7dChart(data.dados);
            }
        } catch (error) {
            console.error('Erro ao carregar dados da estação:', error);
        }
    }

    updateCurrentIndicators(dados) {
        if (dados.length === 0) return;

        // Pega o dado mais recente
        const latest = dados[dados.length - 1];
        
        // Atualiza indicadores atuais
        document.getElementById('current-aqi').textContent = latest.aqi || '--';
        document.getElementById('current-pm25').textContent = latest.pm2_5 ? latest.pm2_5.toFixed(1) : '--';
        document.getElementById('current-pm10').textContent = latest.pm10 ? latest.pm10.toFixed(1) : '--';
        document.getElementById('current-no2').textContent = latest.no2 ? latest.no2.toFixed(1) : '--';
        document.getElementById('current-o3').textContent = latest.o3 ? latest.o3.toFixed(1) : '--';
        document.getElementById('current-so2').textContent = latest.so2 ? latest.so2.toFixed(1) : '--';
        document.getElementById('current-co').textContent = latest.co ? latest.co.toFixed(1) : '--';

        // Atualiza descrição do AQI
        this.updateAQIDescription(latest.aqi);
    }

    updateAQIDescription(aqi) {
        const descriptionElement = document.getElementById('aqi-description');
        const indicatorElement = document.getElementById('current-aqi').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (aqi = 50) {
            description = 'Boa';
            color = '#28a745';
        } else if (aqi <= 100) {
            description = 'Moderada';
            color = '#ffc107';
        } else if (aqi <= 150) {
            description = 'Insalubre';
            color = '#fd7e14';
        } else if (aqi <= 200) {
            description = 'Muito Insalubre';
            color = '#dc3545';
        } else if (aqi <= 300) {
            description = 'Perigosa';
            color = '#6f42c1';
        } else {
            description = 'Muito Perigosa';
            color = '#e83e8c';
        }
        
        descriptionElement.textContent = description;
        indicatorElement.style.borderLeftColor = color;
    }

    update24hChart(dados) {
        // Filtra dados das últimas 24 horas
        const now = new Date();
        const twentyFourHoursAgo = new Date(now.getTime() - (24 * 60 * 60 * 1000));
        
        const last24h = dados.filter(dado => {
            const date = new Date(dado.timestamp);
            return date >= twentyFourHoursAgo;
        });

        const labels = last24h.map(dado => {
            const date = new Date(dado.timestamp);
            return date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        });

        const pm25Data = last24h.map(dado => dado.pm2_5);
        const pm10Data = last24h.map(dado => dado.pm10);
        const no2Data = last24h.map(dado => dado.no2);
        const o3Data = last24h.map(dado => dado.o3);
        const so2Data = last24h.map(dado => dado.so2);
        const coData = last24h.map(dado => dado.co);

        this.charts.grafico24h.data.labels = labels;
        this.charts.grafico24h.data.datasets[0].data = pm25Data;
        this.charts.grafico24h.data.datasets[1].data = pm10Data;
        this.charts.grafico24h.data.datasets[2].data = no2Data;
        this.charts.grafico24h.data.datasets[3].data = o3Data;
        this.charts.grafico24h.data.datasets[4].data = so2Data;
        this.charts.grafico24h.data.datasets[5].data = coData;
        this.charts.grafico24h.update();
    }

    update7dChart(dados) {
        // Agrupa dados por dia
        const dailyData = {};
        dados.forEach(dado => {
            const date = new Date(dado.timestamp);
            const dayKey = date.toISOString().split('T')[0];
            
            if (!dailyData[dayKey]) {
                dailyData[dayKey] = {
                    aqi: [],
                    pm25: [],
                    pm10: [],
                    no2: [],
                    o3: [],
                    so2: [],
                    co: [],
                };
            }
            
            if (dado.aqi) dailyData[dayKey].aqi.push(dado.aqi);
            if (dado.pm2_5) dailyData[dayKey].pm25.push(dado.pm2_5);
            if (dado.pm10) dailyData[dayKey].pm25.push(dado.pm10);
            if (dado.no2) dailyData[dayKey].pm25.push(dado.no2);
            if (dado.o3) dailyData[dayKey].pm25.push(dado.o3);
            if (dado.so2) dailyData[dayKey].pm25.push(dado.so2);
            if (dado.co) dailyData[dayKey].pm25.push(dado.co);
        });

        const labels = Object.keys(dailyData).sort();
        const aqiData = labels.map(day => {
            const values = dailyData[day].aqi;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });
        const pm25Data = labels.map(day => {
            const values = dailyData[day].pm25;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });

        const pm10Data = labels.map(day => {
            const values = dailyData[day].pm10;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });
        const no2Data = labels.map(day => {
            const values = dailyData[day].no2;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });
        const o3Data = labels.map(day => {
            const values = dailyData[day].o3;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });
        const so2Data = labels.map(day => {
            const values = dailyData[day].so2;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });
        const coData = labels.map(day => {
            const values = dailyData[day].co;
            return values.length > 0 ? values.reduce((a, b) => a + b) / values.length : 0;
        });

        // Formata labels para formato mais amigável
        const formattedLabels = labels.map(label => {
            const date = new Date(label);
            return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
        });

        this.charts.grafico7dias.data.labels = formattedLabels;
        this.charts.grafico7dias.data.datasets[0].data = aqiData;
        this.charts.grafico7dias.data.datasets[1].data = pm25Data;
        this.charts.grafico7dias.data.datasets[2].data = pm10Data;
        this.charts.grafico7dias.data.datasets[3].data = no2Data;
        this.charts.grafico7dias.data.datasets[4].data = o3Data;
        this.charts.grafico7dias.data.datasets[5].data = so2Data;
        this.charts.grafico7dias.data.datasets[6].data = coData;
        this.charts.grafico7dias.update();
    }

    clearCharts() {
        // Limpa todos os gráficos e indicadores
        document.getElementById('current-aqi').textContent = '--';
        document.getElementById('current-pm25').textContent = '--';
        document.getElementById('current-pm10').textContent = '--';
        document.getElementById('current-no2').textContent = '--';
        document.getElementById('current-o3').textContent = '--';
        document.getElementById('current-so2').textContent = '--';
        document.getElementById('current-co').textContent = '--';
        document.getElementById('aqi-description').textContent = '--';

        this.charts.grafico24h.data.labels = [];
        this.charts.grafico24h.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.grafico24h.update();

        this.charts.grafico7dias.data.labels = [];
        this.charts.grafico7dias.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.grafico7dias.update();
    }
}

// Inicializa quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.dashboardCharts = new DashboardCharts();
});

// Função global para ser chamada pelos marcadores do mapa
function loadStationChart(stationId) {
    const select = document.getElementById('station-select');
    select.value = stationId;
    window.dashboardCharts.loadStationData(stationId);
}