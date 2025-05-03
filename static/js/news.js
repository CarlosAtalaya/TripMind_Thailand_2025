/**
 * TravelBoard - Funcionalidades relacionadas con noticias
 * 
 * Gestiona la obtención y visualización de noticias relevantes
 */

class NewsService {
    constructor() {
        this.cache = {};
        this.cacheExpiration = 1800000; // 30 minutos en milisegundos
    }

    /**
     * Obtiene noticias para una región específica
     * @param {string} regionId - ID de la región
     * @param {number} maxItems - Número máximo de noticias a obtener
     * @returns {Promise} - Promesa con las noticias
     */
    async getNewsForRegion(regionId, maxItems = 5) {
        // Verificar si tenemos datos en caché y si son válidos
        const cacheKey = `news_${regionId}_${maxItems}`;
        const cachedData = this.cache[cacheKey];
        
        if (cachedData && (Date.now() - cachedData.timestamp < this.cacheExpiration)) {
            console.log('Usando noticias en caché para', regionId);
            return cachedData.data;
        }

        // Si no hay caché o expiró, obtener datos frescos
        try {
            const response = await fetch(`/api/news/${regionId}?max=${maxItems}`);
            if (!response.ok) {
                throw new Error(`Error al obtener noticias: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Guardar en caché
            this.cache[cacheKey] = {
                data: data,
                timestamp: Date.now()
            };
            
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
        const date = new Date(dateString);
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
     * Evalúa la relevancia de una noticia para viajeros
     * @param {Object} article - Artículo de noticia
     * @returns {number} - Puntuación de relevancia (0-100)
     */
    evaluateRelevance(article) {
        // Palabras clave de alta relevancia para viajeros
        const highRelevanceKeywords = [
            'alerta', 'peligro', 'emergencia', 'evacuación', 'cierre',
            'cancelación', 'huelga', 'protesta', 'manifestación',
            'desastre', 'accidente', 'seguridad', 'restricción'
        ];
        
        // Palabras clave de relevancia media
        const mediumRelevanceKeywords = [
            'turismo', 'viajero', 'transporte', 'hotel', 'vuelo',
            'aeropuerto', 'festival', 'evento', 'celebración', 'atracción',
            'museo', 'parque', 'playa', 'montaña', 'covid', 'pandemia'
        ];
        
        let score = 0;
        const content = (article.title + ' ' + article.description).toLowerCase();
        
        // Verificar palabras clave de alta relevancia
        highRelevanceKeywords.forEach(keyword => {
            if (content.includes(keyword)) {
                score += 20;
            }
        });
        
        // Verificar palabras clave de relevancia media
        mediumRelevanceKeywords.forEach(keyword => {
            if (content.includes(keyword)) {
                score += 10;
            }
        });
        
        // Limitar la puntuación a 100
        return Math.min(score, 100);
    }

    /**
     * Renderiza las noticias en un contenedor
     * @param {string} containerId - ID del contenedor HTML
     * @param {Object} newsData - Datos de noticias
     */
    renderNewsData(containerId, newsData) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Si hay un error en los datos o no hay artículos
        if (newsData.error || !newsData.articles || newsData.articles.length === 0) {
            container.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <div class="alert alert-info mb-0">
                            <i class="fas fa-info-circle me-2"></i>
                            No hay noticias relevantes para esta región en este momento.
                        </div>
                    </div>
                </div>
            `;
            return;
        }

        // Evaluar relevancia de cada artículo
        newsData.articles.forEach(article => {
            article.relevance = this.evaluateRelevance(article);
        });
        
        // Ordenar por relevancia (mayor a menor)
        newsData.articles.sort((a, b) => b.relevance - a.relevance);

        // Crear contenido HTML para las noticias
        let html = '<div class="card"><div class="card-body">';

        newsData.articles.forEach(article => {
            // Determinar clase CSS según relevancia
            let relevanceClass = '';
            if (article.relevance >= 60) {
                relevanceClass = 'border-danger';
            } else if (article.relevance >= 30) {
                relevanceClass = 'border-warning';
            }
            
            html += `
                <div class="news-item ${relevanceClass}">
                    <h6 class="mb-1">
                        <a href="${article.url}" target="_blank" rel="noopener noreferrer">
                            ${article.title}
                        </a>
                    </h6>
                    <p class="mb-1 small">
                        ${article.description || ''}
                    </p>
                    <div class="news-source d-flex justify-content-between">
                        <span>${article.source}</span>
                        <span>${this.formatPublishedDate(article.published_at)}</span>
                    </div>
                </div>
            `;
        });

        // Agregar información de actualización
        html += `
            <div class="text-center small text-muted mt-3">
                <i class="fas fa-sync-alt"></i> Actualizado: ${new Date().toLocaleTimeString()}
            </div>
        `;

        html += '</div></div>';
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
            <div class="card">
                <div class="card-body">
                    <div class="text-center py-3">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Cargando...</span>
                        </div>
                        <p class="mt-2 mb-0">Buscando noticias relevantes...</p>
                    </div>
                </div>
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
            <div class="card">
                <div class="card-body">
                    <div class="alert alert-danger mb-0">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        Error: ${errorMessage}
                    </div>
                </div>
            </div>
        `;
    }
}

// Exportar la clase para uso en otros scripts
window.NewsService = NewsService;