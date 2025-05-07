/**
 * TravelBoard - Funcionalidades específicas para móvil
 */

document.addEventListener('DOMContentLoaded', function() {
    // Detectar si es un dispositivo móvil
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile || window.innerWidth <= 768) {
        initMobileFeatures();
    }
    
    // Re-verificar en caso de cambio de orientación
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            initMobileFeatures();
        }
    });
});

function initMobileFeatures() {
    // 1. Mejorar scrolling en iOS
    document.addEventListener('touchmove', function(e) {
        if (e.target.closest('.modal')) {
            e.preventDefault();
        }
    }, { passive: false });
    
    // 2. Cerrar menús al hacer click fuera
    document.addEventListener('touchstart', function(e) {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });
    });
    
    // 3. Mejorar tabs con swipe
    let touchStartX = 0;
    let touchEndX = 0;
    
    const tabContent = document.querySelector('.tab-content');
    if (tabContent) {
        tabContent.addEventListener('touchstart', e => {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        tabContent.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
    }
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            const tabs = document.querySelectorAll('.nav-tabs .nav-link');
            let activeIndex = -1;
            
            tabs.forEach((tab, index) => {
                if (tab.classList.contains('active')) {
                    activeIndex = index;
                }
            });
            
            if (diff > 0 && activeIndex < tabs.length - 1) {
                // Swipe izquierda - siguiente tab
                tabs[activeIndex + 1].click();
            } else if (diff < 0 && activeIndex > 0) {
                // Swipe derecha - tab anterior
                tabs[activeIndex - 1].click();
            }
        }
    }
    
    // 4. Prevenir zoom en inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('touchstart', function() {
            this.style.fontSize = '16px';
        });
    });
    
    // 5. Optimizar imágenes para móvil
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        if (!img.dataset.mobileSrc) return;
        
        if (window.innerWidth <= 768) {
            img.src = img.dataset.mobileSrc;
        }
    });
}

// Función para mostrar/ocultar elementos según orientación
function handleOrientation() {
    const isLandscape = window.orientation === 90 || window.orientation === -90;
    
    if (isLandscape && window.innerWidth <= 768) {
        document.body.classList.add('mobile-landscape');
    } else {
        document.body.classList.remove('mobile-landscape');
    }
}

window.addEventListener('orientationchange', handleOrientation);