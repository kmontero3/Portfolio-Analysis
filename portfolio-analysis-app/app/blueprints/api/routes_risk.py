"""
Portfolio Risk Analysis Routes

Handles risk metrics and analysis calculations.
"""

from flask import jsonify, request
from app.blueprints.api import api_bp
from app.blueprints.api.schwab_integration import SchwabAPIError
from app.blueprints.api.routes_auth import get_schwab_client


@api_bp.route('/portfolio/risk', methods=['GET'])
def get_portfolio_risk():
    """
    Calculate portfolio risk metrics.
    
    Query Parameters:
        account_hash (optional): Filter by specific account
        
    Returns:
        JSON: Risk analysis including diversification, concentration, etc.
    """
    try:
        schwab_client = get_schwab_client()
        account_hash = request.args.get('account_hash')
        
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        portfolio_data = schwab_client.get_portfolio_data(account_hash=account_hash)
        
        # Extract positions for risk calculation
        positions = []
        if isinstance(portfolio_data, list):
            for account in portfolio_data:
                securities_account = account.get('securitiesAccount', {})
                account_positions = securities_account.get('positions', [])
                positions.extend(account_positions)
        else:
            securities_account = portfolio_data.get('securitiesAccount', {})
            positions = securities_account.get('positions', [])
        
        # Calculate risk metrics
        risk_metrics = calculate_risk_metrics(positions)
        
        return jsonify({
            'success': True,
            'data': risk_metrics
        }), 200
        
    except SchwabAPIError as e:
        return jsonify({
            'success': False,
            'error': 'API Error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Error',
            'message': str(e)
        }), 500


@api_bp.route('/portfolio/analyze', methods=['POST'])
def analyze_portfolio():
    """
    Perform comprehensive portfolio analysis.
    
    Request Body:
        JSON: Analysis parameters and options
        
    Returns:
        JSON: Comprehensive portfolio analysis results
    """
    data = request.json
    
    try:
        schwab_client = get_schwab_client()
        
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        # Get portfolio data
        account_hash = data.get('account_hash') if data else None
        portfolio_data = schwab_client.get_portfolio_data(account_hash=account_hash)
        
        # Perform analysis
        analysis_results = perform_portfolio_analysis(portfolio_data, data)
        
        return jsonify({
            'success': True,
            'data': analysis_results
        }), 200
        
    except SchwabAPIError as e:
        return jsonify({
            'success': False,
            'error': 'API Error',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Error',
            'message': str(e)
        }), 500


def calculate_risk_metrics(positions):
    """
    Calculate risk metrics for a list of positions.
    
    Args:
        positions: List of position dictionaries
        
    Returns:
        dict: Risk metrics including concentration, diversification, etc.
    """
    if not positions:
        return {
            'total_positions': 0,
            'concentration_risk': 'N/A',
            'diversification_score': 0,
            'largest_position_pct': 0,
            'top_holdings': []
        }
    
    # Calculate total portfolio value
    total_value = sum(pos.get('marketValue', 0) for pos in positions)
    
    if total_value == 0:
        return {
            'total_positions': len(positions),
            'concentration_risk': 'N/A',
            'diversification_score': 0,
            'largest_position_pct': 0,
            'top_holdings': []
        }
    
    # Calculate position percentages
    position_data = []
    for pos in positions:
        market_value = pos.get('marketValue', 0)
        percentage = (market_value / total_value) * 100 if total_value > 0 else 0
        
        instrument = pos.get('instrument', {})
        symbol = instrument.get('symbol', 'Unknown')
        
        position_data.append({
            'symbol': symbol,
            'value': market_value,
            'percentage': round(percentage, 2)
        })
    
    # Sort by value descending
    position_data.sort(key=lambda x: x['value'], reverse=True)
    
    # Calculate concentration risk
    largest_pct = position_data[0]['percentage'] if position_data else 0
    top_5_pct = sum(p['percentage'] for p in position_data[:5])
    
    if largest_pct > 20:
        concentration = 'High'
    elif largest_pct > 10:
        concentration = 'Medium'
    else:
        concentration = 'Low'
    
    # Calculate diversification score (0-100)
    # Higher score = better diversification
    num_positions = len(positions)
    if num_positions >= 20:
        base_score = 100
    elif num_positions >= 10:
        base_score = 75
    elif num_positions >= 5:
        base_score = 50
    else:
        base_score = 25
    
    # Adjust for concentration
    if largest_pct > 30:
        base_score -= 30
    elif largest_pct > 20:
        base_score -= 20
    elif largest_pct > 10:
        base_score -= 10
    
    diversification_score = max(0, min(100, base_score))
    
    return {
        'total_positions': num_positions,
        'concentration_risk': concentration,
        'diversification_score': diversification_score,
        'largest_position_pct': round(largest_pct, 2),
        'top_5_concentration': round(top_5_pct, 2),
        'top_holdings': position_data[:10]  # Top 10 holdings
    }


def perform_portfolio_analysis(portfolio_data, options=None):
    """
    Perform comprehensive portfolio analysis.
    
    Args:
        portfolio_data: Portfolio data from Schwab API
        options: Analysis options and parameters
        
    Returns:
        dict: Comprehensive analysis results
    """
    options = options or {}
    
    # Extract positions
    positions = []
    if isinstance(portfolio_data, list):
        for account in portfolio_data:
            securities_account = account.get('securitiesAccount', {})
            account_positions = securities_account.get('positions', [])
            positions.extend(account_positions)
    else:
        securities_account = portfolio_data.get('securitiesAccount', {})
        positions = securities_account.get('positions', [])
    
    # Calculate various metrics
    risk_metrics = calculate_risk_metrics(positions)
    
    # Calculate asset allocation
    asset_allocation = calculate_asset_allocation(positions)
    
    # Calculate performance metrics (if data available)
    performance = calculate_performance_metrics(positions)
    
    return {
        'risk_analysis': risk_metrics,
        'asset_allocation': asset_allocation,
        'performance': performance,
        'timestamp': datetime.now().isoformat()
    }


def calculate_asset_allocation(positions):
    """
    Calculate asset allocation by asset class.
    
    Args:
        positions: List of position dictionaries
        
    Returns:
        dict: Asset allocation percentages
    """
    total_value = sum(pos.get('marketValue', 0) for pos in positions)
    
    if total_value == 0:
        return {}
    
    # Group by asset type
    allocation = {}
    for pos in positions:
        instrument = pos.get('instrument', {})
        asset_type = instrument.get('assetType', 'Unknown')
        market_value = pos.get('marketValue', 0)
        
        if asset_type in allocation:
            allocation[asset_type] += market_value
        else:
            allocation[asset_type] = market_value
    
    # Convert to percentages
    allocation_pct = {}
    for asset_type, value in allocation.items():
        allocation_pct[asset_type] = round((value / total_value) * 100, 2)
    
    return allocation_pct


def calculate_performance_metrics(positions):
    """
    Calculate performance metrics for positions.
    
    Args:
        positions: List of position dictionaries
        
    Returns:
        dict: Performance metrics
    """
    total_cost = 0
    total_value = 0
    gains = 0
    losses = 0
    
    for pos in positions:
        market_value = pos.get('marketValue', 0)
        average_price = pos.get('averagePrice', 0)
        quantity = pos.get('longQuantity', 0)
        
        cost_basis = average_price * quantity
        total_cost += cost_basis
        total_value += market_value
        
        gain_loss = market_value - cost_basis
        if gain_loss > 0:
            gains += gain_loss
        else:
            losses += abs(gain_loss)
    
    total_gain_loss = total_value - total_cost
    total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
    
    return {
        'total_cost_basis': round(total_cost, 2),
        'total_market_value': round(total_value, 2),
        'total_gain_loss': round(total_gain_loss, 2),
        'total_return_pct': round(total_return_pct, 2),
        'total_gains': round(gains, 2),
        'total_losses': round(losses, 2),
        'win_loss_ratio': round(gains / losses, 2) if losses > 0 else float('inf')
    }


# Import datetime for timestamps
from datetime import datetime
