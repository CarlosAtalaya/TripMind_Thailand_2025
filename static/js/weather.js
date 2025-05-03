/**
 * TravelBoard - Funcionalidades relacionadas con el clima
 * 
 * Gestiona la obtención y visualización de datos meteorológicos
 */

class WeatherService {
    constructor() {
        this.cache = {};
        this.cacheExpiration = 3600000; // 1 hora en milisegundos
    }

    /**
     * Obtiene los datos del clima para una región
     * @param {string} regionId - ID de la región
     * @param {number} days - Número de días para el pronóstico
     * @returns {Promise} - Promesa con los datos del clima
     */
    async getWeatherForRegion(regionId, days = 3) {
        // Verificar si tenemos datos en caché y si son válidos
        const cacheKey = `weather_${regionId}_${days}`;
        const cachedData = this.cache[cacheKey];
        
        if (cachedData && (Date.now() - cachedData.timestamp < this.cacheExpiration)) {
            console.log('Usando datos de clima en caché para', regionId);
            return cachedData.data;
        }

        // Si no hay caché o expiró, obtener datos frescos
        try {
            const response = await fetch(`/api/weather/${regionId}?days=${days}`);
            if (!response.ok) {
                throw new Error(`Error al obtener clima: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Guardar en caché
            this.cache[cacheKey] = {
                data: data,
                timestamp: Date.now()
            };
            
            return data;
        } catch (error) {
            console.error('Error al obtener datos del clima:', error);
            throw error;
        }
    }

    /**
     * Obtiene el ícono adecuado para un código de clima
     * @param {number} code - Código de clima de OpenMeteo
     * @returns {string} - Clase de ícono Font Awesome
     */
    getWeatherIcon(code) {
        // Mapeo de códigos a íconos
        if (code <= 1) return 'fa-sun'; // Despejado
        if (code <= 3) return 'fa-cloud-sun'; // Parcialmente nublado
        if (code <= 48) return 'fa-cloud'; // Nublado, niebla
        if (code <= 55) return 'fa-cloud-rain'; // Llovizna
        if (code <= 65) return 'fa-cloud-showers-heavy'; // Lluvia
        if (code <= 77) return 'fa-snowflake'; // Nieve
        if (code <= 82) return 'fa-cloud-rain'; // Chubascos
        if (code <= 86) return 'fa-snowflake'; // Nieve
        if (code <= 99) return 'fa-bolt'; // Tormenta
        
        return 'fa-cloud'; // Por defecto
    }

    /**
     * Renderiza los datos del clima en un contenedor
     * @param {string} containerId - ID del contenedor HTML
     * @param {Object} weatherData - Datos del clima
     */
    renderWeatherData(containerId, weatherData) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Si hay un error en los datos
        if (weatherData.error) {
            container.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Error: ${weatherData.error}
                </div>
            `;
            return;
        }

        // Crear contenido HTML para el pronóstico
        let html = '<div class="row">';

        weatherData.forecast.forEach(day => {
            const date = new Date(day.date);
            const formattedDate = date.toLocaleDateString('es-ES', { 
                weekday: 'short', 
                day: 'numeric',
                month: 'short'
            });

            html += `
                <div class="col-6 col-md-4 col-lg text-center mb-3">
                    <div class="card h-100">
                        <div class="card-body p-2">
                            <div class="fw-bold">${formattedDate}</div>
                            <div class="weather-icon my-2">
                                <i class="fas ${this.getWeatherIcon(day.weather_code)}"></i>
                            </div>
                            <div class="temp">
                                <span class="temp-max">${day.temp_max}°C</span> / 
                                <span class="temp-min">${day.temp_min}°C</span>
                            </div>
                            <div class="precipitation small">
                                <i class="fas fa-tint"></i> ${day.precipitation} mm
                            </div>
                            <div class="weather-desc small text-muted">
                                ${day.weather_description}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        
        // Agregar información de actualización
        html += `
            <div class="text-center small text-muted mt-2">
                <i class="fas fa-sync-alt"></i> Actualizado: ${new Date().toLocaleTimeString()}
            </div>
        `;

        container.innerHTML = html;
    }

    /**
     * Renderiza un estado de carga en el contenedor
     * @param {string} containerId - ID del contenedor HTML
     */
    renderLoadingState(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Obteniendo datos del clima...</p>
            </div>
        `;
    }

    /**
     * Renderiza un estado de error en el contenedor
     * @param {string} containerId - ID del contenedor HTML
     * @param {string} errorMessage - Mensaje de error
     */
    renderErrorState(containerId, errorMessage) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error: ${errorMessage}
            </div>
        `;
    }
}

// Exportar la clase para uso en otros scripts
window.WeatherService = WeatherService;