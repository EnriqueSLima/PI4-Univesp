
document.addEventListener('DOMContentLoaded', function() {
    // Dados mock - gerados para visualização
    const mockData = {
        ciclovias: 450,
        distritos: 96,
        subprefeituras: 32,
        regioes: {
            labels: ['Centro', 'Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste'],
            data: [25, 20, 30, 15, 10],
            colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        },
        evolucao: {
            anos: ['2018', '2019', '2020', '2021', '2022', '2023'],
            ciclovias: [120, 180, 250, 320, 390, 450],
            areasVerdes: [45, 48, 52, 55, 58, 60]
        },
        tipos: {
            labels: ['Ciclovias Protegidas', 'Ciclofaixas', 'Ciclorrotas', 'Compartilhadas'],
            data: [35, 25, 20, 20],
            colors: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
        }
    };
    
    // Atualizar estatísticas
    document.getElementById('ciclovias-count').textContent = mockData.ciclovias;
    document.getElementById('distritos-count').textContent = mockData.distritos;
    document.getElementById('subprefeituras-count').textContent = mockData.subprefeituras;
    
    // Gráfico 1: Pizza - Distribuição por Região
    const regiaoCtx = document.getElementById('regiaoChart').getContext('2d');
    new Chart(regiaoCtx, {
        type: 'pie',
        data: {
            labels: mockData.regioes.labels,
            datasets: [{
                data: mockData.regioes.data,
                backgroundColor: mockData.regioes.colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Distribuição por Região'
                }
            }
        }
    });
    
    // Gráfico 2: Linha - Evolução Temporal
    const evolucaoCtx = document.getElementById('evolucaoChart').getContext('2d');
    new Chart(evolucaoCtx, {
        type: 'line',
        data: {
            labels: mockData.evolucao.anos,
            datasets: [
                {
                    label: 'Ciclovias (km)',
                    data: mockData.evolucao.ciclovias,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Áreas Verdes',
                    data: mockData.evolucao.areasVerdes,
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução da Infraestrutura'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Gráfico 3: Barras - Comparação por Tipo
    const tipoCtx = document.getElementById('tipoChart').getContext('2d');
    new Chart(tipoCtx, {
        type: 'bar',
        data: {
            labels: mockData.tipos.labels,
            datasets: [{
                data: mockData.tipos.data,
                backgroundColor: mockData.tipos.colors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Tipos de Infraestrutura Cicloviária'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quantidade'
                    }
                }
            }
        }
    });
});
