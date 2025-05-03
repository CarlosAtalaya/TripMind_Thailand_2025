/**
 * TravelBoard - Funcionalidades relacionadas con votaciones
 * 
 * Gestiona la obtención y visualización de rankings de votaciones
 */

class VotesService {
    constructor() {
        this.cache = null;
        this.cacheTimestamp = 0;
        this.cacheExpiration = 300000; // 5 minutos en milisegundos
    }

    /**
     * Obtiene los rankings de todas las categorías
     * @param {number} days - Número de días para filtrar resultados
     * @returns {Promise} - Promesa con los rankings
     */
    async getRankings(days = 7) {
        // Verificar si tenemos datos en caché y si son válidos
        const cacheKey = `rankings_${days}`;
        if (this.cache && this.cache[cacheKey] && (Date.now() - this.cacheTimestamp < this.cacheExpiration)) {
            console.log('Usando rankings en caché');
            return this.cache[cacheKey];
        }

        // Si no hay caché o expiró, obtener datos frescos
        try {
            const response = await fetch(`/votes/api/rankings?days=${days}`);
            if (!response.ok) {
                throw new Error(`Error al obtener rankings: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Guardar en caché
            if (!this.cache) this.cache = {};
            this.cache[cacheKey] = data;
            this.cacheTimestamp = Date.now();
            
            return data;
        } catch (error) {
            console.error('Error al obtener rankings:', error);
            throw error;
        }
    }

    /**
     * Renderiza un selector de categorías
     * @param {string} containerId - ID del contenedor HTML
     * @param {function} onCategoryChange - Función a llamar cuando se cambia la categoría
     */
    async renderCategorySelector(containerId, onCategoryChange) {
        const container = document.getElementById(containerId);
        if (!container) return;

        try {
            const rankings = await this.getRankings();
            
            // Crear selector
            let html = `
                <div class="mb-3">
                    <select class="form-select" id="${containerId}-select">
                        <option value="">Selecciona una categoría...</option>
            `;
            
            // Añadir opciones
            for (const categoryName in rankings) {
                html += `<option value="${categoryName}">${categoryName}</option>`;
            }
            
            html += `
                    </select>
                </div>
                <div id="${containerId}-content"></div>
            `;
            
            container.innerHTML = html;
            
            // Configurar evento de cambio
            const select = document.getElementById(`${containerId}-select`);
            select.addEventListener('change', function() {
                const selectedCategory = this.value;
                if (selectedCategory && rankings[selectedCategory]) {
                    onCategoryChange(rankings[selectedCategory], selectedCategory);
                } else {
                    document.getElementById(`${containerId}-content`).innerHTML = `
                        <div class="text-center py-3">
                            <p class="text-muted">Selecciona una categoría para ver el ranking</p>
                        </div>
                    `;
                }
            });
        } catch (error) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Error al cargar las categorías. Por favor, intenta de nuevo.
                </div>
            `;
        }
    }

    /**
     * Renderiza un ranking de categoría
     * @param {string} containerId - ID del contenedor HTML
     * @param {Array} ranking - Datos del ranking
     * @param {string} categoryName - Nombre de la categoría
     */
    renderRanking(containerId, ranking, categoryName) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Ordenar por puntos
        const sortedRanking = [...ranking].sort((a, b) => b.points - a.points);
        
        if (sortedRanking.length === 0 || sortedRanking[0].points === 0) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay votos aún para la categoría "${categoryName}".
                </div>
            `;
            return;
        }
        
        // Crear el HTML del ranking
        let html = '<div class="list-group">';
        
        sortedRanking.forEach((traveler, index) => {
            // Definir clase para el podio
            let badgeClass = 'bg-secondary';
            let icon = '';
            
            if (index === 0) {
                badgeClass = 'bg-warning text-dark'; // Oro
                icon = '<i class="fas fa-trophy text-warning me-2"></i>';
            } else if (index === 1) {
                badgeClass = 'bg-light text-dark'; // Plata
                icon = '<i class="fas fa-medal text-secondary me-2"></i>';
            } else if (index === 2) {
                badgeClass = 'bg-danger'; // Bronce
                icon = '<i class="fas fa-award text-danger me-2"></i>';
            }
            
            html += `
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <span>${icon}${traveler.name}</span>
                    <span class="badge ${badgeClass} rounded-pill">${traveler.points} pts</span>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    /**
     * Renderiza todos los rankings en un contenedor
     * @param {string} containerId - ID del contenedor HTML
     * @param {number} days - Número de días para filtrar resultados
     */
    async renderAllRankings(containerId, days = 7) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Mostrar estado de carga
        container.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando rankings...</p>
            </div>
        `;
        
        try {
            const rankings = await this.getRankings(days);
            
            // Crear contenedor de tarjetas
            let html = '<div class="row row-cols-1 row-cols-md-2 g-4">';
            
            // Crear una tarjeta para cada categoría
            for (const [categoryName, ranking] of Object.entries(rankings)) {
                // Ordenar por puntos
                const sortedRanking = [...ranking].sort((a, b) => b.points - a.points);
                
                html += `
                    <div class="col">
                        <div class="card h-100">
                            <div class="card-header">
                                <h5 class="mb-0">${categoryName}</h5>
                            </div>
                            <div class="card-body">
                `;
                
                if (sortedRanking.length === 0 || sortedRanking[0].points === 0) {
                    html += `
                        <div class="text-center py-3">
                            <i class="fas fa-info-circle fa-2x text-muted mb-3"></i>
                            <p>No hay votos para esta categoría en el período seleccionado.</p>
                        </div>
                    `;
                } else {
                    html += `
                        <ol class="list-group list-group-numbered">
                    `;
                    
                    sortedRanking.slice(0, 5).forEach(traveler => {
                        html += `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div class="ms-2 me-auto">
                                    <div class="fw-bold">${traveler.name}</div>
                                </div>
                                <span class="badge bg-primary rounded-pill">${traveler.points} pts</span>
                            </li>
                        `;
                    });
                    
                    html += `
                        </ol>
                    `;
                }
                
                html += `
                            </div>
                        </div>
                    </div>
                `;
            }
            
            html += '</div>';
            container.innerHTML = html;
        } catch (error) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Error al cargar los rankings. Por favor, intenta de nuevo.
                </div>
            `;
        }
    }
}

// Exportar la clase para uso en otros scripts
window.VotesService = VotesService;