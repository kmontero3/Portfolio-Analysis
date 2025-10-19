/**
 * Portfolio Analysis Application - Main JavaScript
 * 
 * This file handles application initialization and core functionality
 */

// Global app state
const AppState = {
    isAuthenticated: false,
    portfolioData: null,
    accounts: null,
    lastUpdate: null
};

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('Initializing Portfolio Analysis Application...');
    
    // Check authentication status
    checkAuthStatus();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize tooltips if needed
    initializeTooltips();
}

/**
 * Check authentication status with Schwab API
 */
async function checkAuthStatus() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    try {
        const response = await API.getAuthStatus();
        
        if (response.success && response.data.authenticated) {
            AppState.isAuthenticated = true;
            if (statusIndicator) {
                statusIndicator.classList.add('connected');
                statusIndicator.classList.remove('disconnected');
            }
            if (statusText) {
                statusText.textContent = 'Connected';
            }
        } else {
            AppState.isAuthenticated = false;
            if (statusIndicator) {
                statusIndicator.classList.add('disconnected');
                statusIndicator.classList.remove('connected');
            }
            if (statusText) {
                statusText.textContent = 'Not Connected';
            }
        }
    } catch (error) {
        console.error('Failed to check auth status:', error);
        AppState.isAuthenticated = false;
        if (statusIndicator) {
            statusIndicator.classList.add('disconnected');
            statusIndicator.classList.remove('connected');
        }
        if (statusText) {
            statusText.textContent = 'Error';
        }
    }
}

/**
 * Set up global event listeners
 */
function setupEventListeners() {
    // Handle modal clicks outside content
    window.onclick = function(event) {
        const modal = document.getElementById('authModal');
        if (event.target === modal) {
            closeAuthModal();
        }
    };
    
    // Handle escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeAuthModal();
        }
    });
}

/**
 * Initialize tooltips (if using a tooltip library)
 */
function initializeTooltips() {
    // Placeholder for tooltip initialization
    // Can be extended with libraries like Tippy.js
}

/**
 * Show authentication modal
 */
function showAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.classList.add('active');
    }
}

/**
 * Close authentication modal
 */
function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

/**
 * Start authentication flow
 */
async function startAuth() {
    try {
        showLoading('Getting authorization URL...');
        const response = await API.getAuthUrl();
        hideLoading();
        
        if (response.success && response.data.authorization_url) {
            // Open authorization URL in new window
            window.open(response.data.authorization_url, '_blank');
            
            // Update modal content
            const modalContent = document.getElementById('authModalContent');
            if (modalContent) {
                modalContent.innerHTML = `
                    <div class="alert alert-info">
                        <p>A new window has been opened for authorization.</p>
                        <p>After authorizing, this page will automatically refresh.</p>
                    </p>
                    <button onclick="checkAuthStatus()" class="btn btn-secondary">Check Status</button>
                `;
            }
            
            // Start checking for successful auth
            startAuthPolling();
        } else {
            showAlert('Failed to get authorization URL', 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Auth error:', error);
        showAlert('Authentication failed: ' + error.message, 'error');
    }
}

/**
 * Poll for successful authentication
 */
function startAuthPolling() {
    const pollInterval = setInterval(async () => {
        const response = await API.getAuthStatus();
        
        if (response.success && response.data.authenticated) {
            clearInterval(pollInterval);
            closeAuthModal();
            showAlert('Successfully authenticated!', 'success');
            
            // Reload the page to show authenticated content
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    }, 3000); // Check every 3 seconds
    
    // Stop polling after 5 minutes
    setTimeout(() => {
        clearInterval(pollInterval);
    }, 300000);
}

/**
 * Show loading overlay
 * @param {string} message - Loading message to display
 */
function showLoading(message = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        const textElement = overlay.querySelector('p');
        if (textElement) {
            textElement.textContent = message;
        }
        overlay.classList.add('active');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

/**
 * Show alert message
 * @param {string} message - Message to display
 * @param {string} type - Alert type (success, error, warning, info)
 */
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        const alertDiv = document.createElement('div');
        alertDiv.innerHTML = alertHtml;
        container.insertBefore(alertDiv.firstElementChild, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.firstElementChild.remove();
        }, 5000);
    }
}

/**
 * Format currency
 * @param {number} value - Value to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

/**
 * Format percentage
 * @param {number} value - Value to format
 * @returns {string} Formatted percentage string
 */
function formatPercentage(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value / 100);
}

/**
 * Format number with commas
 * @param {number} value - Value to format
 * @returns {string} Formatted number string
 */
function formatNumber(value) {
    return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// Export functions for use in other modules
window.AppState = AppState;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showAlert = showAlert;
window.formatCurrency = formatCurrency;
window.formatPercentage = formatPercentage;
window.formatNumber = formatNumber;
window.showAuthModal = showAuthModal;
window.closeAuthModal = closeAuthModal;
window.startAuth = startAuth;
