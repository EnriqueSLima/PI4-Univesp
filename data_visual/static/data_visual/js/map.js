// Script para forçar altura do mapa

function forceMapHeight() {
    // Encontrar todos os elementos possíveis do mapa
    const elements = [
        document.getElementById('map-container'),
        document.querySelector('.folium-map'),
        document.querySelector('.leaflet-container'),
        document.querySelector('.map')
    ];
    
    elements.forEach(el => {
        if (el) {
            el.style.height = '100vh';
            el.style.minHeight = '100vh';
        }
    });
    
    // Forçar iframes também
    const iframes = document.querySelectorAll('iframe');
    iframes.forEach(iframe => {
        iframe.style.height = '100vh';
        iframe.style.width = '100%';
    });
    
    // Redimensionar mapa Leaflet
    if (typeof map !== 'undefined') {
        setTimeout(() => {
            map.invalidateSize();
            map._onResize();
        }, 100);
    }
}

// Executar múltiplas vezes
document.addEventListener('DOMContentLoaded', forceMapHeight);
window.addEventListener('load', forceMapHeight);
setTimeout(forceMapHeight, 500);
setTimeout(forceMapHeight, 1000);
setTimeout(forceMapHeight, 2000);
