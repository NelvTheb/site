function openLightbox(imageSrc) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    
    lightboxImg.src = imageSrc;
    
    // Détection automatique : l'URL se termine-t-elle par .svg ?
    if (imageSrc.toLowerCase().endsWith('.svg')) {
        lightboxImg.classList.add('is-svg');
    } else {
        lightboxImg.classList.remove('is-svg');
    }
    
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden'; 
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    
    lightbox.classList.remove('active');
    
    // On nettoie la classe SVG pour la prochaine ouverture
    lightboxImg.classList.remove('is-svg');
    
    document.body.style.overflow = ''; 
}