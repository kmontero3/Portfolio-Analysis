/**
 * Portfolio Analysis Application - API Module
 * 
 * This module handles all API communication with the backend
 */

const API = {
    baseUrl: '/api',
    
    /**
     * Make an API request
     * @param {string} endpoint - API endpoint
     * @param {object} options - Fetch options
     * @returns {Promise<object>} API response
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const fetchOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, fetchOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    /**
     * GET request
     * @param {string} endpoint - API endpoint
     * @returns {Promise<object>} API response
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },
    
    /**
     * POST request
     * @param {string} endpoint - API endpoint
     * @param {object} data - Request body data
     * @returns {Promise<object>} API response
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
    
    // ===========================
    // Authentication Endpoints
    // ===========================
    
    /**
     * Get authentication status
     * @returns {Promise<object>} Auth status
     */
    async getAuthStatus() {
        return this.get('/auth/status');
    },
    
    /**
     * Get authorization URL
     * @returns {Promise<object>} Authorization URL
     */
    async getAuthUrl() {
        return this.get('/auth/url');
    },
    
    /**
     * Get all accounts
     * @returns {Promise<object>} List of accounts
     */
    async getAccounts() {
        return this.get('/accounts');
    },
    
    /**
     * Get specific account data
     * @param {string} accountHash - Account hash
     * @param {string} fields - Fields to include (e.g., 'positions')
     * @returns {Promise<object>} Account data
     */
    async getAccount(accountHash, fields = 'positions') {
        return this.get(`/account/${accountHash}?fields=${fields}`);
    },
    
    // ===========================
    // Portfolio Endpoints
    // ===========================
    
    /**
     * Get portfolio data
     * @param {string} accountHash - Optional account hash
     * @returns {Promise<object>} Portfolio data
     */
    async getPortfolio(accountHash = null) {
        const url = accountHash ? `/portfolio?account_hash=${accountHash}` : '/portfolio';
        return this.get(url);
    },
    
    /**
     * Get portfolio positions
     * @param {string} accountHash - Optional account hash
     * @returns {Promise<object>} Portfolio positions
     */
    async getPositions(accountHash = null) {
        const url = accountHash ? `/portfolio/positions?account_hash=${accountHash}` : '/portfolio/positions';
        return this.get(url);
    },
    
    /**
     * Get portfolio summary
     * @param {string} accountHash - Optional account hash
     * @returns {Promise<object>} Portfolio summary
     */
    async getPortfolioSummary(accountHash = null) {
        const url = accountHash ? `/portfolio/summary?account_hash=${accountHash}` : '/portfolio/summary';
        return this.get(url);
    },
    
    // ===========================
    // Risk Analysis Endpoints
    // ===========================
    
    /**
     * Get portfolio risk analysis
     * @param {string} accountHash - Optional account hash
     * @returns {Promise<object>} Risk analysis
     */
    async getPortfolioRisk(accountHash = null) {
        const url = accountHash ? `/portfolio/risk?account_hash=${accountHash}` : '/portfolio/risk';
        return this.get(url);
    },
    
    /**
     * Analyze portfolio
     * @param {object} options - Analysis options
     * @returns {Promise<object>} Analysis results
     */
    async analyzePortfolio(options = {}) {
        return this.post('/portfolio/analyze', options);
    },
};

// Export API object
window.API = API;
