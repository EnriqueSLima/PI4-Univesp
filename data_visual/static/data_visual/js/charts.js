// Gráficos e funcionalidades do dashboard
class DashboardCharts {
    constructor() {
        this.currentStationId = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.loadEstatisticasGerais();
        this.setupEventListeners();
        this.initCharts();
    }

    setupEventListeners() {
        document.getElementById('station-select').addEventListener('change', (e) => {
            this.currentStationId = e.target.value;
            if (this.currentStationId) {
                this.loadStationData(this.currentStationId);
            } else {
                this.clearCharts();
            }
        });
    }

    async loadStationData(stationId) {
        try {
            const response = await fetch(`/api/estacao/${stationId}/`);
            const data = await response.json();
            
            if (data.success) {
                console.log('Dados recebidos:', data.dados); // DEBUG
                this.analyzeDataStructure(data.dados); // DEBUG
                this.updateCurrentIndicators(data.dados);
                this.update24hChart(data.dados);
                this.update7dChart(data.dados);
            }
        } catch (error) {
            console.error('Erro ao carregar dados da estação:', error);
        }
    }

    // Função para analisar a estrutura dos dados
    analyzeDataStructure(dados) {
        if (dados.length === 0) {
            console.log('Nenhum dado disponível');
            return;
        }

        console.log('=== ANÁLISE DOS DADOS ===');
        console.log('Total de registros:', dados.length);
        
        // Verificar período dos dados
        const timestamps = dados.map(d => new Date(d.timestamp));
        const minDate = new Date(Math.min(...timestamps));
        const maxDate = new Date(Math.max(...timestamps));
        console.log('Período:', minDate.toLocaleString(), 'até', maxDate.toLocaleString());
        
        // Verificar frequência dos dados
        const timeDiffs = [];
        for (let i = 1; i < timestamps.length; i++) {
            const diff = (timestamps[i] - timestamps[i-1]) / (1000 * 60); // diferença em minutos
            timeDiffs.push(diff);
        }
        
        if (timeDiffs.length > 0) {
            const avgDiff = timeDiffs.reduce((a, b) => a + b) / timeDiffs.length;
            console.log('Frequência média (minutos):', avgDiff.toFixed(1));
        }
        
        // Verificar campos disponíveis
        const sample = dados[0];
        console.log('Campos disponíveis:', Object.keys(sample));
        console.log('=== FIM DA ANÁLISE ===');
    }

    initCharts() {
        // Gráfico das últimas 24 horas - MAIS FLEXÍVEL
        const particulas24h = document.getElementById('particulas-24h').getContext('2d');
        this.charts.particulas24h = new Chart(particulas24h, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'PM2.5',
                        data: [],
                        borderColor: 'lightgray',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                    {
                        label: 'PM10',
                        data: [],
                        borderColor: 'darkgray',
                        backgroundColor: 'rgba(255, 162, 235, 0.1)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Material Particulado (PM2.5 e PM10)'
                    },
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
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
                            text: 'Hora'
                        }
                    }
                }
            }
        });

        // Gráfico das últimas 24 horas - MAIS FLEXÍVEL
        const gases24h = document.getElementById('gases-24h').getContext('2d');
        this.charts.gases24h = new Chart(gases24h, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'CO',
                        data: [],
                        borderColor: '#0072B2',
                        backgroundColor: 'rgba(45, 146, 223, 1)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                    {
                        label: 'O³',
                        data: [],
                        borderColor: '#009E73',
                        backgroundColor: 'rgba(26, 199, 95, 1)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Monóxido de Carbono (CO) e Ozônio (O³)'
                    },
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
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
                            text: 'Hora'
                        }
                    }
                }
            }
        });

        // Gráfico das últimas 24 horas - MAIS FLEXÍVEL
        const gasesb24h = document.getElementById('gasesb-24h').getContext('2d');
        this.charts.gasesb24h = new Chart(gasesb24h, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'NO²',
                        data: [],
                        borderColor: '#E69F00',
                        backgroundColor: 'rgba(244, 147, 73, 0.99)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                    {
                        label: 'SO²',
                        data: [],
                        borderColor: '#FFCE56',
                        backgroundColor: 'rgba(235, 226, 54, 0.94)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 2,
                        pointRadius: 3
                    },
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Dióxido de Nitrogênio (NO²) e Dióxido de Enxofre (SO²)'
                    },
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
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
                            text: 'Hora'
                        }
                    }
                }
            }
        });

        // Gráfico dos últimos 7 dias - MÉDIAS DIÁRIAS
        const ctx7d = document.getElementById('grafico-7dias').getContext('2d');
        this.charts.grafico7dias = new Chart(ctx7d, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'AQI Médio',
                        data: [],
                        borderColor: '#E74C3C',
                        backgroundColor: 'rgba(231, 77, 60, 0.81)',
                        borderWidth: 3,
                        fill: false,
                        tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'PM2.5 Médio',
                        data: [],
                        borderColor: '#FF6384',
                        backgroundColor: 'rgba(255, 99, 133, 0.8)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        yAxisID: 'y1'
                    },
                    {
                        label: 'PM10 Médio',
                        data: [],
                        borderColor: '#36A2EB',
                        backgroundColor: 'rgba(54, 163, 235, 0.79)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Médias Diárias'
                    },
                    legend: {
                        position: 'top',
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'AQI'
                        },
                        grid: {
                            drawOnChartArea: true,
                        },
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Poluentes (µg/m³)'
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Data'
                        }
                    }
                }
            }
        });
    }

    async loadEstatisticasGerais() {
        try {
            const response = await fetch('/api/estatisticas-gerais/');
            const data = await response.json();
            
            document.getElementById('estacao-count').textContent = data.estacoes_count;
            document.getElementById('distritos-count').textContent = data.distritos_count;
            document.getElementById('subprefeituras-count').textContent = data.subprefeituras_count;
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
        }
    }

    updateCurrentIndicators(dados) {
        if (dados.length === 0) {
            this.clearIndicators();
            return;
        }

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
        this.updatePM25Description(latest.pm2_5);
        this.updatePM10Description(latest.pm10);
        this.updateO3Description(latest.o3);
        this.updateCODescription(latest.co);
        this.updateNO2Description(latest.no2);
        this.updateSO2Description(latest.so2);
    }

// Função que avalia o AQI
    updateAQIDescription(aqi) {
        const descriptionElement = document.getElementById('aqi-description');
        const indicatorElement = document.getElementById('current-aqi').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (aqi <= 1) {
            description = 'Boa';
            color = '#28a745';
        } else if (aqi <= 2) {
            description = 'Moderada';
            color = '#ffc107';
        } else if (aqi <= 3) {
            description = 'Insalubre';
            color = '#fd7e14';
        } else if (aqi <= 4) {
            description = 'Muito Insalubre';
            color = '#dc3545';
        } else if (aqi <= 5) {
            description = 'Perigosa';
            color = '#6f42c1';
        } else {
            description = 'Muito Perigosa';
            color = '#e83e8c';
        }
        
        descriptionElement.textContent = description;
        indicatorElement.style.borderLeftColor = color;
    }

// Função que avalia PM2.5
    updatePM25Description(pm2_5) {
        const indicatorPM25 = document.getElementById('current-pm25').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (pm2_5 <= 15) {
            color = '#28a745';
        } else if (pm2_5 <= 30) {
            color = '#ffc107';
        } else if (pm2_5 <= 55) {
            color = '#fd7e14';
        } else if (pm2_5 = 110) {
            color = '#dc3545';
        } else {
            color = '#6f42c1';
        }
        indicatorPM25.style.borderLeftColor = color;
    }

// Função que avalia PM10
    updatePM10Description(pm10) {
        const indicatorElement = document.getElementById('current-pm10').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (pm10 <= 45) {
            color = '#28a745';
        } else if (pm10 <= 90) {
            color = '#ffc107';
        } else if (pm10 <= 150) {
            color = '#fd7e14';
        } else if (pm10 <= 250) {
            color = '#dc3545';
        } else {
            color = '#6f42c1';
        }        
        indicatorElement.style.borderLeftColor = color;
    }

// Função que avalia O³
    updateO3Description(o3) {
        const indicatorElement = document.getElementById('current-o3').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (o3 <= 100) {
            color = '#28a745';
        } else if (o3 <= 130) {
            color = '#ffc107';
        } else if (o3 <= 160) {
            color = '#fd7e14';
        } else if (o3 <=200) {
            color = '#dc3545';
        } else if (o3 > 200) {
            color = '#6f42c1';
        }        
        indicatorElement.style.borderLeftColor = color;
    }
// Função que avalia CO
    updateCODescription(co) {
        const indicatorElement = document.getElementById('current-co').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (co <= 4) {
            color = '#28a745';
        } else if (co <= 9) {
            color = '#ffc107';
        } else if (co <= 15) {
            color = '#fd7e14';
        } else if (co <= 30) {
            color = '#dc3545';
        } else if (co > 30) {
            color = '#6f42c1';
        }        
        indicatorElement.style.borderLeftColor = color;
    }
// Função que avalia NO²
    updateNO2Description(no2) {
        const indicatorElement = document.getElementById('current-no2').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (no2 <= 40) {
            color = '#28a745';
        } else if (no2 <= 80) {
            color = '#ffc107';
        } else if (no2 <= 180) {
            color = '#fd7e14';
        } else if (no2 <= 280) {
            color = '#dc3545';
        } else if (no2 > 280) {
            color = '#6f42c1';
        }        
        indicatorElement.style.borderLeftColor = color;
    }

// Função que avalia SO²
    updateSO2Description(so2) {
        const indicatorElement = document.getElementById('current-so2').parentElement;
        
        let description = '--';
        let color = '#6c757d';
        
        if (so2 <= 50) {
            color = '#28a745';
        } else if (so2 <= 100) {
            color = '#ffc107';
        } else if (so2 <= 250) {
            color = '#fd7e14';
        } else if (so2 <= 350) {
            color = '#dc3545';
        } else if (so2 >350) {
            color = '#6f42c1';
        } 
        indicatorElement.style.borderLeftColor = color;
    }

// Função que atualiza todos os gráficos di dia
    update24hChart(dados) {
        if (dados.length === 0) {
            this.clearChart24h();
            return;
        }
        // Pega dados das últimas 24 horas
        const now = new Date();
        const twentyFourHoursAgo = new Date(now.getTime() - (24 * 60 * 60 * 1000));
        // Filtra os dados das ultimas 24h
        const last24h = dados.filter(dado => {
            const date = new Date(dado.timestamp);
            return date >= twentyFourHoursAgo;
        });
        // Log para DEBUG
        console.log('Dados das últimas 24h:', last24h.length, 'registros');
        if (last24h.length === 0) {
            // Se não há dados das últimas 24h, usa os últimos dados disponíveis (máx 10)
            const recentData = dados.slice(-10);
            this.updateChartWithAvailableData(this.charts.grafico24h, recentData, 'Dados Recentes Disponíveis');
            return;
        }
        // Formata labels baseado na frequência dos dados
        const labels = this.formatLabelsBasedOnFrequency(last24h);
        // Cria constantes para os dados das ultimas 24h
        const pm25Data = last24h.map(dado => dado.pm2_5 || 0);
        const pm10Data = last24h.map(dado => dado.pm10 || 0);
        const o3Data = last24h.map(dado => dado.o3 || 0);
        const coData = last24h.map(dado => dado.co || 0);
        const no2Data = last24h.map(dado => dado.no2 || 0);
        const so2Data = last24h.map(dado => dado.so2 || 0);
        // Coloca os dados no gráfico de partículas
        this.charts.particulas24h.data.labels = labels;
        this.charts.particulas24h.data.datasets[0].data = pm25Data;
        this.charts.particulas24h.data.datasets[1].data = pm10Data;
        // Coloca os dados no gráfico de gases
        this.charts.gases24h.data.labels = labels;
        this.charts.gases24h.data.datasets[0].data = o3Data;
        this.charts.gases24h.data.datasets[1].data = coData;
        // Coloca os dados no gráfico de gasesb
        this.charts.gasesb24h.data.labels = labels;
        this.charts.gasesb24h.data.datasets[0].data = no2Data;
        this.charts.gasesb24h.data.datasets[1].data = so2Data;
        
        // Atualiza título baseado nos dados disponíveis
        //this.charts.grafico24h.options.plugins.title.text = `Variação dos Poluentes (${last24h.length} registros)`;
        //this.charts.gases24h.options.plugins.title.text = `Variação dos Poluentes (${last24h.length} registros)`;
        
        this.charts.particulas24h.update();
        this.charts.gases24h.update();
        this.charts.gasesb24h.update();
    }

// Função que atualiza os dados da semana
    update7dChart(dados) {
        if (dados.length === 0) {
            this.clearChart7d();
            return;
        }
        // Agrupa dados por dia e calcula médias
        const dailyData = this.calculateDailyAverages(dados);
        
        const labels = Object.keys(dailyData).sort();
        const aqiData = labels.map(day => dailyData[day].aqi || 0);
        const pm25Data = labels.map(day => dailyData[day].pm25 || 0);
        const pm10Data = labels.map(day => dailyData[day].pm10 || 0);
        // Formata labels para formato mais amigável
        const formattedLabels = labels.map(label => {
            const date = new Date(label);
            return date.toLocaleDateString('pt-BR', { 
                day: '2-digit', 
                month: '2-digit',
                weekday: 'short'
            });
        });
        this.charts.grafico7dias.data.labels = formattedLabels;
        this.charts.grafico7dias.data.datasets[0].data = aqiData;
        this.charts.grafico7dias.data.datasets[1].data = pm25Data;
        this.charts.grafico7dias.data.datasets[2].data = pm10Data;
        
        // Atualiza título
        this.charts.grafico7dias.options.plugins.title.text = `Tendência Semanal (${labels.length} dias)`;
        
        this.charts.grafico7dias.update();
    }

// Função auxiliar para formatar labels baseado na frequência dos dados
    formatLabelsBasedOnFrequency(dados) {
        if (dados.length === 0) return [];
        
        if (dados.length === 1) {
            // Apenas um ponto - mostra data completa
            const date = new Date(dados[0].timestamp);
            return [date.toLocaleString('pt-BR')];
        }
        
        // Verifica se os dados são do mesmo dia
        const firstDate = new Date(dados[0].timestamp);
        const lastDate = new Date(dados[dados.length - 1].timestamp);
        const sameDay = firstDate.toDateString() === lastDate.toDateString();
        
        if (sameDay && dados.length <= 6) {
            // Poucos pontos no mesmo dia - mostra hora:minuto
            return dados.map(dado => {
                const date = new Date(dado.timestamp);
                return date.toLocaleTimeString('pt-BR', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
            });
        } else {
            // Múltiplos dias ou muitos pontos - mostra data reduzida
            return dados.map(dado => {
                const date = new Date(dado.timestamp);
                return date.toLocaleDateString('pt-BR', { 
                    day: '2-digit', 
                    month: '2-digit',
                    hour: '2-digit'
                });
            });
        }
    }

// Função para calcular médias diárias
    calculateDailyAverages(dados) {
        const dailyData = {};
        
        dados.forEach(dado => {
            const date = new Date(dado.timestamp);
            const dayKey = date.toISOString().split('T')[0]; // YYYY-MM-DD
            
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
            if (dado.pm10) dailyData[dayKey].pm10.push(dado.pm10);
            if (dado.no2) dailyData[dayKey].no2.push(dado.no2);
            if (dado.o3) dailyData[dayKey].o3.push(dado.o3);
            if (dado.so2) dailyData[dayKey].so2.push(dado.so2);
            if (dado.co) dailyData[dayKey].co.push(dado.co);
        });

        // Calcula médias
        const result = {};
        Object.keys(dailyData).forEach(day => {
            result[day] = {
                aqi: dailyData[day].aqi.length > 0 ? 
                    dailyData[day].aqi.reduce((a, b) => a + b) / dailyData[day].aqi.length : null,
                pm25: dailyData[day].pm25.length > 0 ? 
                    dailyData[day].pm25.reduce((a, b) => a + b) / dailyData[day].pm25.length : null,
                pm10: dailyData[day].pm10.length > 0 ? 
                    dailyData[day].pm10.reduce((a, b) => a + b) / dailyData[day].pm10.length : null
            };
        });

        return result;
    }

// Função para atualizar gráfico com dados disponíveis
    updateChartWithAvailableData(chart, dados, title) {
        const labels = dados.map(dado => {
            const date = new Date(dado.timestamp);
            return date.toLocaleString('pt-BR', { 
                day: '2-digit',
                month: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        });
        // Dados gráfico de partículas
        const pm25Data = dados.map(dado => dado.pm2_5 || 0);
        const pm10Data = dados.map(dado => dado.pm10 || 0);
        // Dados gráfico de gases
        const o3Data = dados.map(dado => dado.o3 || 0);
        const coData = dados.map(dado => dado.co || 0);
        // Dados gráfico de gasesb
        const no2Data = dados.map(dado => dado.no2 || 0);
        const so2Data = dados.map(dado => dado.so2 || 0);

        chart.data.labels = labels;
        chart.data.datasets[0].data = pm25Data;
        chart.data.datasets[1].data = pm10Data;
        chart.data.datasets[2].data = no2Data;
        chart.data.datasets[3].data = o3Data;
        chart.data.datasets[4].data = coData;
        chart.data.datasets[5].data = so2Data;
        chart.options.plugins.title.text = title;
        chart.update();
    }

// Função para limpar os indicadores
    clearIndicators() {
        document.getElementById('current-aqi').textContent = '--';
        document.getElementById('current-pm25').textContent = '--';
        document.getElementById('current-pm10').textContent = '--';
        document.getElementById('current-no2').textContent = '--';
        document.getElementById('current-o3').textContent = '--';
        document.getElementById('current-so2').textContent = '--';
        document.getElementById('current-co').textContent = '--';
        document.getElementById('aqi-description').textContent = '--';
    }

// Função para limpar os graficos do dia
    clearChart24h() {
        // Para gráfico particulas
        this.charts.particulas24h.data.labels = [];
        this.charts.particulas24h.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.particulas24h.options.plugins.title.text = 'Sem dados disponíveis';
        this.charts.particulas24h.update();
        // Para gráfico gases
        this.charts.gases24h.data.labels = [];
        this.charts.gases24h.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.gases24h.options.plugins.title.text = 'Sem dados disponíveis';
        this.charts.gases24h.update();
        // Para gráfico gasesb
        this.charts.gasesb24h.data.labels = [];
        this.charts.gasesb24h.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.gasesb24h.options.plugins.title.text = 'Sem dados disponíveis';
        this.charts.gasesb24h.update();
    }

// Função para limpar os graficos da semana
    clearChart7d() {
        this.charts.grafico7dias.data.labels = [];
        this.charts.grafico7dias.data.datasets.forEach(dataset => dataset.data = []);
        this.charts.grafico7dias.options.plugins.title.text = 'Sem dados disponíveis';
        this.charts.grafico7dias.update();
    }

//Função que limpa todos os campos de gráficos
    clearCharts() {
        this.clearIndicators();
        this.clearChart24h();
        this.clearChart7d();
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