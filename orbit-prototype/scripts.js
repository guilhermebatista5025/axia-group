/**
 * AXIA Orbit Prototype Interactions
 */

function openProjectPreview(pageSrc, mockAddressUrl) {
  const modal = document.getElementById('project-modal');
  const iframe = document.getElementById('project-iframe');
  const addressText = document.getElementById('browser-url-text');
  const loader = document.getElementById('iframe-loader');

  if (modal && iframe && addressText && loader) {
    // Show loading spinner
    loader.classList.remove('hidden');
    
    // Set custom browser-bar address URL
    addressText.textContent = mockAddressUrl;

    // Load sub-page inside iframe
    iframe.src = pageSrc;

    // Open modal container
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
  }
}

function closeProjectPreview() {
  const modal = document.getElementById('project-modal');
  const iframe = document.getElementById('project-iframe');

  if (modal) {
    // Close modal
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    
    // Clear iframe src after delay to stop operations
    setTimeout(() => {
      if (iframe) iframe.src = "";
    }, 300);
  }
}

function hideIframeLoader() {
  const loader = document.getElementById('iframe-loader');
  if (loader) {
    // Hide spinner once loading concludes
    loader.classList.add('hidden');
  }
}

// Global listener: Keyboard Esc closes preview modal
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeProjectPreview();
  }
});
