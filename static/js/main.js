/**
 * TravelBoard - Script principal
 * 
 * Funcionalidades principales del frontend para TravelBoard MVP
 */

// Función principal al cargar el documento
// Función principal al cargar el documento
document.addEventListener('DOMContentLoaded', function() {
    // Activar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // NUEVO: Manejar el cierre del menú en móvil
    const navbarCollapse = document.querySelector('#mainNav');
    const navLinks = document.querySelectorAll('#mainNav .nav-link:not(.dropdown-toggle)');
    const dropdownItems = document.querySelectorAll('#mainNav .dropdown-item');
    
    // Cerrar menú al hacer clic en un enlace normal
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            // Solo cerrar si estamos en móvil y el navbar está expandido
            if (window.innerWidth < 992) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse && navbarCollapse.classList.contains('show')) {
                    bsCollapse.hide();
                }
            }
        });
    });
    
    // Cerrar menú al hacer clic en un item del dropdown
    dropdownItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                // Permitir que el enlace funcione antes de cerrar
                setTimeout(function() {
                    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                    if (bsCollapse && navbarCollapse.classList.contains('show')) {
                        bsCollapse.hide();
                    }
                }, 100);
            }
        });
    });
    
    // NUEVO: Prevenir el cierre automático del dropdown en móvil
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('hide.bs.dropdown', function(e) {
            // Si estamos en móvil, evitar que se cierre automáticamente
            if (window.innerWidth < 992 && e.clickEvent) {
                e.preventDefault();
                
                // Si se hizo clic en un enlace del dropdown, permitir la navegación
                if (e.clickEvent.target.closest('.dropdown-item')) {
                    const link = e.clickEvent.target.closest('.dropdown-item');
                    if (link.href) {
                        // Dar tiempo para que se ejecute la navegación
                        setTimeout(function() {
                            window.location.href = link.href;
                        }, 100);
                    }
                }
            }
        });
    });

    // Detectar la posición de scroll para resaltar enlaces del navbar
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        // Obtener todas las secciones de regiones
        const regionSections = document.querySelectorAll('.region-card');
        const overviewSection = document.getElementById('overview');
        
        // Verificar si estamos en la sección de resumen
        if (overviewSection && scrollPosition < overviewSection.offsetTop + overviewSection.offsetHeight - 100) {
            setActiveNavItem('overview');
            return;
        }
        
        // Verificar cada sección de región
        regionSections.forEach(function(section) {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop - 100 && scrollPosition < sectionTop + sectionHeight - 100) {
                const sectionId = section.id;
                setActiveNavItem(sectionId);
            }
        });
    });

    // Establecer el enlace activo en la navegación
    function setActiveNavItem(sectionId) {
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(function(link) {
            link.classList.remove('active');
            
            const href = link.getAttribute('href');
            if (href && href.substring(1) === sectionId) {
                link.classList.add('active');
            }
        });
    }

    // Inicializar el formato de fechas para toda la aplicación
    initializeDateFormatting();

    // Animar elementos cuando aparecen en el viewport
    initializeScrollAnimations();
});

/**
 * Inicializa el formato de fechas en toda la aplicación
 */
function initializeDateFormatting() {
    // Formatear todas las fechas con formato ISO
    document.querySelectorAll('.iso-date').forEach(function(element) {
        const isoDate = element.textContent;
        if (isoDate && isoDate.match(/^\d{4}-\d{2}-\d{2}/)) {
            const date = new Date(isoDate);
            element.textContent = date.toLocaleDateString('es-ES', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    });
}

/**
 * Inicializa animaciones al hacer scroll
 */
function initializeScrollAnimations() {
    // Detectar elementos para animar
    const elementsToAnimate = document.querySelectorAll('.animate-on-scroll');
    
    // Configurar el observador de intersección
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observar cada elemento
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Función para mostrar mensajes de alerta
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de alerta (success, warning, danger, info)
 * @param {number} duration - Duración en milisegundos
 */
function showAlert(message, type = 'info', duration = 3000) {
    // Crear elemento de alerta
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show fixed-top mx-auto mt-5`;
    alertElement.style.width = '80%';
    alertElement.style.maxWidth = '500px';
    alertElement.style.zIndex = '9999';
    alertElement.role = 'alert';
    
    // Agregar contenido
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Agregar al body
    document.body.appendChild(alertElement);
    
    // Configurar bootstrap alert
    const bsAlert = new bootstrap.Alert(alertElement);
    
    // Eliminar después de la duración
    if (duration > 0) {
        setTimeout(() => {
            bsAlert.close();
        }, duration);
    }
    
    // Eliminar del DOM después de ocultarse
    alertElement.addEventListener('closed.bs.alert', function() {
        alertElement.remove();
    });
}