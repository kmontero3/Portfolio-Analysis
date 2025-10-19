/**
 * Portfolio Analysis Application - Overview Charts
 * 
 * This module handles chart creation and updates for the overview page
 */

// Chart instances
let assetAllocationChart = null;
let topHoldingsChart = null;

/**
 * Initialize the overview page
 */
async function initializeOverview() {
    console.log('Initializing overview page...');
    
    // Check if user is authenticated
    if (!AppState.isAuthenticated) {
        showAuthModal();
        return;
    }
    
    // Load portfolio data
    await loadPortfolioData();
    
    // Set up refresh handler
    setupRefreshHandler();
}

/**
 * Load portfolio data from API
 */
async function loadPortfolioData() {
    try {
        showLoading('Loading portfolio data...');
        
        // Fetch portfolio summary
        const summaryResponse = await API.getPortfolioSummary();
        if (summaryResponse.success) {
            updateSummaryCards(summaryResponse.data);
        }
        
        // Fetch portfolio positions
        const positionsResponse = await API.getPositions();
        if (positionsResponse.success) {
            updateHoldingsTable(positionsResponse.data.positions);
            createCharts(positionsResponse.data.positions);
        }
        
        // Fetch risk analysis
        const riskResponse = await API.getPortfolioRisk();
        if (riskResponse.success) {
            updateRiskMetrics(riskResponse.data);
        }
        
        AppState.lastUpdate = new Date();
        hideLoading();
    } catch (error) {
        console.error('Failed to load portfolio data:', error);
        hideLoading();
        showAlert('Failed to load portfolio data. Please refresh the page.', 'error');
    }
}

/**
 * Update summary cards with portfolio data
 * @param {object} data - Portfolio summary data
 */
function updateSummaryCards(data) {
    // Total Value
    const totalValueEl = document.getElementById('totalValue');
    if (totalValueEl) {
        totalValueEl.textContent = formatCurrency(data.total_value || 0);
    }
    
    // Total Positions
    const totalPositionsEl = document.getElementById('totalPositions');
    if (totalPositionsEl) {
        totalPositionsEl.textContent = formatNumber(data.total_positions || 0);
    }
    
    // Account Count
    const accountCountEl = document.getElementById('accountCount');
    if (accountCountEl) {
        accountCountEl.textContent = formatNumber(data.total_accounts || 0);
    }
    
    // Cash Balance
    const cashBalanceEl = document.getElementById('cashBalance');
    if (cashBalanceEl) {
        cashBalanceEl.textContent = formatCurrency(data.total_cash || 0);
    }
}

/**
 * Update holdings table with positions data
 * @param {Array} positions - Array of position objects
 */
function updateHoldingsTable(positions) {
    const tableBody = document.getElementById('holdingsTableBody');
    if (!tableBody) return;
    
    if (!positions || positions.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" class="loading-cell">
                    <p>No positions found</p>
                </td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    positions.forEach(position => {
        const instrument = position.instrument || {};
        const symbol = instrument.symbol || 'N/A';
        const description = instrument.description || 'Unknown';
        const quantity = position.longQuantity || 0;
        const currentPrice = position.currentDayProfitLoss / quantity || position.averagePrice || 0;
        const marketValue = position.marketValue || 0;
        const costBasis = position.averagePrice * quantity || 0;
        const gainLoss = marketValue - costBasis;
        const returnPct = costBasis > 0 ? (gainLoss / costBasis) * 100 : 0;
        
        const gainLossClass = gainLoss >= 0 ? 'positive' : 'negative';
        
        html += `
            <tr>
                <td><strong>${symbol}</strong></td>
                <td>${description}</td>
                <td>${formatNumber(quantity)}</td>
                <td>${formatCurrency(currentPrice)}</td>
                <td>${formatCurrency(marketValue)}</td>
                <td>${formatCurrency(costBasis)}</td>
                <td class="change ${gainLossClass}">${formatCurrency(gainLoss)}</td>
                <td class="change ${gainLossClass}">${formatPercentage(returnPct)}</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Create charts for asset allocation and top holdings
 * @param {Array} positions - Array of position objects
 */
function createCharts(positions) {
    if (!positions || positions.length === 0) return;
    
    // Prepare data for charts
    const positionData = positions.map(pos => ({
        symbol: pos.instrument?.symbol || 'Unknown',
        value: pos.marketValue || 0,
        assetType: pos.instrument?.assetType || 'Unknown'
    })).sort((a, b) => b.value - a.value);
    
    // Create asset allocation chart
    createAssetAllocationChart(positionData);
    
    // Create top holdings chart
    createTopHoldingsChart(positionData.slice(0, 10));
}

/**
 * Create asset allocation pie chart
 * @param {Array} positionData - Position data for chart
 */
function createAssetAllocationChart(positionData) {
    const canvas = document.getElementById('assetAllocationChart');
    if (!canvas) return;
    
    // Aggregate by asset type
    const assetTypes = {};
    positionData.forEach(pos => {
        if (!assetTypes[pos.assetType]) {
            assetTypes[pos.assetType] = 0;
        }
        assetTypes[pos.assetType] += pos.value;
    });
    
    const labels = Object.keys(assetTypes);
    const data = Object.values(assetTypes);
    const colors = [
        '#667eea',
        '#764ba2',
        '#f093fb',
        '#4facfe',
        '#43e97b',
        '#fa709a',
        '#fee140',
        '#30cfd0'
    ];
    
    // Destroy existing chart if it exists
    if (assetAllocationChart) {
        assetAllocationChart.destroy();
    }
    
    assetAllocationChart = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(2);
                            return `${label}: ${formatCurrency(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create top holdings bar chart
 * @param {Array} topPositions - Top position data for chart
 */
function createTopHoldingsChart(topPositions) {
    const canvas = document.getElementById('topHoldingsChart');
    if (!canvas) return;
    
    const labels = topPositions.map(pos => pos.symbol);
    const data = topPositions.map(pos => pos.value);
    
    // Destroy existing chart if it exists
    if (topHoldingsChart) {
        topHoldingsChart.destroy();
    }
    
    topHoldingsChart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Market Value',
                data: data,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return formatCurrency(context.parsed.x);
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
}

/**
 * Update risk metrics display
 * @param {object} riskData - Risk analysis data
 */
function updateRiskMetrics(riskData) {
    // Diversification score
    const diversificationProgress = document.getElementById('diversificationProgress');
    const diversificationScore = document.getElementById('diversificationScore');
    if (diversificationProgress && diversificationScore) {
        const score = riskData.diversification_score || 0;
        diversificationProgress.style.width = `${score}%`;
        diversificationScore.textContent = `${score}/100`;
    }
    
    // Concentration risk
    const concentrationBadge = document.getElementById('concentrationBadge');
    if (concentrationBadge) {
        const risk = riskData.concentration_risk || 'N/A';
        concentrationBadge.textContent = risk;
        concentrationBadge.className = 'badge ' + risk.toLowerCase();
    }
    
    // Largest position
    const largestPosition = document.getElementById('largestPosition');
    if (largestPosition) {
        const pct = riskData.largest_position_pct || 0;
        largestPosition.textContent = `${pct.toFixed(2)}%`;
    }
}

/**
 * Set up refresh handler
 */
function setupRefreshHandler() {
    // Add search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterTable, 300));
    }
    
    // Add sort functionality
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', sortTable);
    }
}

/**
 * Filter holdings table based on search input
 */
function filterTable() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const tableBody = document.getElementById('holdingsTableBody');
    const rows = tableBody.getElementsByTagName('tr');
    
    for (let row of rows) {
        const symbol = row.cells[0]?.textContent.toLowerCase() || '';
        const description = row.cells[1]?.textContent.toLowerCase() || '';
        
        if (symbol.includes(searchTerm) || description.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}

/**
 * Sort holdings table
 */
function sortTable() {
    const sortBy = document.getElementById('sortSelect').value;
    // Implement sorting logic based on selection
    // This is a placeholder for now
    console.log('Sorting by:', sortBy);
}

/**
 * Refresh all data
 */
async function refreshData() {
    await loadPortfolioData();
    showAlert('Data refreshed successfully', 'success');
}

// Export functions
window.initializeOverview = initializeOverview;
window.refreshData = refreshData;
