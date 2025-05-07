/**
 * TravelBoard - Funcionalidades para noticias globales
 * 
 * Gestiona la obtención y visualización de noticias relevantes para todo el itinerario
 */

class GlobalNewsService {
    constructor() {
        this.cache = null;
        this.cacheTimestamp = 0;
        this.cacheExpiration = 1800000; // 30 minutos en milisegundos
    }

    /**
     * Obtiene noticias para todo el itinerario
     * @param {number} maxItems - Número máximo de noticias a obtener
     * @param {string} itineraryName - Nombre del archivo del itinerario
     * @returns {Promise} - Promesa con las noticias
     */
    async getAllNews(maxItems = 50, itineraryName = 'thailand_2025.yaml') {
        // Verificar si tenemos datos en caché y si son válidos
        if (this.cache && (Date.now() - this.cacheTimestamp < this.cacheExpiration)) {
            console.log('Usando noticias en caché');
            return this.cache;
        }

        // Si no hay caché o expiró, obtener datos frescos
        try {
            const response = await fetch(`/api/news/all?max=${maxItems}&name=${itineraryName}`);
            if (!response.ok) {
                throw new Error(`Error al obtener noticias: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Guardar en caché
            this.cache = data;
            this.cacheTimestamp = Date.now();
            
            return data;
        } catch (error) {
            console.error('Error al obtener noticias:', error);
            throw error;
        }
    }

    /**
     * Formatea una fecha de publicación
     * @param {string} dateString - Fecha en formato ISO
     * @returns {string} - Fecha formateada
     */
    formatPublishedDate(dateString) {
        if (!dateString) return 'Fecha desconocida';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Si no se puede parsear, devolver el original
        
        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        
        // Si es hoy
        if (diffDays === 0) {
            return `Hoy, ${date.toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}`;
        }
        
        // Si es ayer
        if (diffDays === 1) {
            return `Ayer, ${date.toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}`;
        }
        
        // Si es esta semana
        if (diffDays < 7) {
            return date.toLocaleDateString('es-ES', {weekday: 'long'}) + 
                   `, ${date.toLocaleTimeString('es-ES', {hour: '2-digit', minute:'2-digit'})}`;
        }
        
        // Otros casos
        return date.toLocaleDateString('es-ES', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    }

    /**
     * Evalúa la importancia de una noticia para viajeros
     * @param {Object} article - Artículo de noticia
     * @returns {string} - Clase CSS para indicar importancia
     */
    getAlertClass(article) {
        const highAlertKeywords = [
            // Emergencias extremas
            'emergency', 'evacuation', 'danger', 'terrorist', 'attack', 
            'earthquake', 'tsunami', 'explosion', 'shooting', 'bomb', 
            'violence', 'crisis', 'death', 'killed', 'fatality', 
            'critical', 'severe', 'disaster', 'catastrophe', 'collapse',
            
            // COVID y pandemias
            'outbreak', 'pandemic', 'quarantine', 'lockdown',
            
            // Situaciones muy graves
            'hostage', 'kidnapping', 'murder', 'fire',
            'volcano', 'eruption', 'destroyed',
            
            // Cierres críticos
            'airport closed', 'border closed', 'travel ban', 'do not travel',
            'tourist killed', 'tourist arrested', 'tourist missing'
        ];
        
        const mediumAlertKeywords = [
            // Seguridad y orden público  
            'alert', 'security', 'protest', 'demonstration', 'strike',
            'police', 'military', 'curfew', 'incident', 'accident',
            'crash', 'theft', 'robbery', 'pickpocket', 'scam',
            'arrest', 'jail', 'detained', 'fine', 'penalty',
            
            // Salud
            'covid', 'virus', 'disease', 'infection', 'hospital',
            'medical', 'health', 'dengue', 'malaria', 'fever',
            'vaccination', 'sick', 'doctor', 'clinic',
            'food poisoning', 'stomach', 'diarrhea',
            
            // Clima y condiciones
            'storm', 'rain', 'flood', 'weather', 'monsoon',
            'typhoon', 'cyclone', 'landslide', 'drought', 'heatwave',
            'temperature', 'humidity', 'forecast', 'season', 'tropical storm',
            
            // Transporte
            'flight', 'canceled', 'cancelled', 'delayed', 'closure',
            'traffic', 'road closure', 'transport', 'ferry', 'train', 'bus',
            'airport', 'disruption', 'breakdown',
            
            // Turismo y viajes
            'tourist', 'tourism', 'visa', 'immigration', 'embassy', 
            'consulate', 'passport', 'backpacker', 'hotel', 'hostel',
            'overstay', 'deportation', 'entry denied',
            
            // Cultura y entretenimiento
            'ladyboy', 'kathoey', 'nightlife', 'red light', 'ping pong show',
            'full moon party', 'massage parlor', 'happy ending', 'tuk tuk',
            'tourist trap', 'bar girl', 'go go bar', 'soapy massage',
            'karaoke', 'walking street', 'party', 'fiesta', 'alcohol',
            'drunk', 'drugs', 'marijuana', 'cannabis', 'mushrooms',
            'police raid', 'bar', 'club',
            
            // Términos específicos
            'spanish tourist', 'spanish group', 'español', 'españoles',
            'turista español', 'group tour', 'money', 'atm', 'credit card',
            'temple', 'buddha', 'monk', 'festival', 'celebration', 'holiday',
            'beach', 'island', 'diving', 'snorkeling', 'boat', 'speedboat',
            
            // Términos graciosos/informales
            'guiri', 'borracho', 'borrachera', 'resaca', 'juerga',
            'cagalera', 'cagar', 'vomitar', 'ligar', 'prostituta', 'burdel'
        ];
        
        const content = (article.title + ' ' + article.description).toLowerCase();
        
        // Verificar alertas altas primero
        for (const keyword of highAlertKeywords) {
            if (content.includes(keyword.toLowerCase())) {
                return 'border-danger';
            }
        }
        
        // Luego verificar alertas medias
        for (const keyword of mediumAlertKeywords) {
            if (content.includes(keyword.toLowerCase())) {
                return 'border-warning';
            }
        }
        
        return '';  // Borde azul por defecto
    }

    /**
     * Renderiza las noticias en el contenedor global
     * @param {Object} newsData - Datos de noticias
     */
    renderNewsData(newsData) {
        const container = document.getElementById('global-news-container');
        if (!container) return;

        // Si hay un error en los datos o no hay artículos
        if (!newsData.articles || newsData.articles.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info m-3">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay noticias relevantes para tu viaje en este momento.
                </div>
            `;
            return;
        }

        // Crear contenido HTML para las noticias
        let html = '<div class="news-list">';

        newsData.articles.forEach(article => {
            const alertClass = this.getAlertClass(article);
            
            html += `
                <div class="news-item p-3 border-bottom ${alertClass}">
                    <h6 class="mb-1">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                            ${article.title}
                        </a>
                    </h6>
                    <p class="mb-1 small">
                        ${article.description || ''}
                    </p>
                    <div class="news-source d-flex justify-content-between">
                        <span class="small text-muted">${article.source}</span>
                        <span class="small text-muted">${this.formatPublishedDate(article.publishedAt)}</span>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;
        
        // Actualizar la hora de última actualización
        const updateElement = document.getElementById('news-last-updated');
        if (updateElement) {
            updateElement.textContent = `Actualizado: ${new Date().toLocaleTimeString()}`;
        }
    }

    /**
     * Renderiza un estado de error en el contenedor
     * @param {string} errorMessage - Mensaje de error
     */
    renderErrorState(errorMessage) {
        const container = document.getElementById('global-news-container');
        if (!container) return;

        container.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error: ${errorMessage}
            </div>
        `;
    }
}

// Inicializar el servicio cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    const globalNewsService = new GlobalNewsService();
    
    // Obtener el nombre del itinerario de un elemento data o usar el valor por defecto
    const itineraryElement = document.getElementById('itinerary-data');
    const itineraryName = itineraryElement ? itineraryElement.dataset.name : 'thailand_2025.yaml';
    
    // Cargar noticias para el contenedor principal
    globalNewsService.getAllNews(50, itineraryName)
        .then(data => {
            // Renderizar en el contenedor principal (sidebar)
            globalNewsService.renderNewsData(data);
            
            // NUEVO: También renderizar en el contenedor móvil si existe
            const mobileContainer = document.getElementById('mobile-news-container');
            if (mobileContainer) {
                globalNewsService.renderMobileNewsData(data);
            }
        })
        .catch(error => {
            globalNewsService.renderErrorState('No se pudieron cargar las noticias');
            
            // NUEVO: También mostrar error en móvil
            const mobileContainer = document.getElementById('mobile-news-container');
            if (mobileContainer) {
                globalNewsService.renderMobileErrorState('No se pudieron cargar las noticias');
            }
            
            console.error('Error al cargar noticias globales:', error);
        });
    
    // NUEVO: Añadir métodos para renderizar en móvil
    GlobalNewsService.prototype.renderMobileNewsData = function(newsData) {
        const container = document.getElementById('mobile-news-container');
        if (!container) return;

        // Si hay un error en los datos o no hay artículos
        if (!newsData.articles || newsData.articles.length === 0) {
            container.innerHTML = `
                <div class="alert alert-info m-3">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay noticias relevantes para tu viaje en este momento.
                </div>
            `;
            return;
        }

        // Crear contenido HTML para las noticias
        let html = '<div class="news-list">';

        newsData.articles.forEach(article => {
            const alertClass = this.getAlertClass(article);
            
            html += `
                <div class="news-item p-3 border-bottom ${alertClass}">
                    <h6 class="mb-1">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                            ${article.title}
                        </a>
                    </h6>
                    <p class="mb-1 small">
                        ${article.description || ''}
                    </p>
                    <div class="news-source d-flex justify-content-between">
                        <span class="small text-muted">${article.source}</span>
                        <span class="small text-muted">${this.formatPublishedDate(article.publishedAt)}</span>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;
        
        // Actualizar la hora de última actualización
        const updateElement = document.getElementById('mobile-news-last-updated');
        if (updateElement) {
            updateElement.textContent = `Actualizado: ${new Date().toLocaleTimeString()}`;
        }
    };
    
    GlobalNewsService.prototype.renderMobileErrorState = function(errorMessage) {
        const container = document.getElementById('mobile-news-container');
        if (!container) return;

        container.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="fas fa-exclamation-circle me-2"></i>
                Error: ${errorMessage}
            </div>
        `;
    };
});