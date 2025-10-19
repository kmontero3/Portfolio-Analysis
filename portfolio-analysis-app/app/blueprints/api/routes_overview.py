"""
Portfolio Overview Routes

Handles portfolio data retrieval and overview information.
"""

from flask import jsonify, request
from app.blueprints.api import api_bp
from app.blueprints.api.schwab_integration import SchwabClient, SchwabAPIError
from app.blueprints.api.routes_auth import get_schwab_client


@api_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    """
    Get portfolio data for the authenticated user.
    
    Query Parameters:
        account_hash (optional): Specific account hash to query
        
    Returns:
        JSON: Portfolio data including positions and balances
    """
    try:
        schwab_client = get_schwab_client()
        account_hash = request.args.get('account_hash')
        
        # Ensure client is authenticated
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        portfolio_data = schwab_client.get_portfolio_data(account_hash=account_hash)
        return jsonify({
            'success': True,
            'data': portfolio_data
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


@api_bp.route('/portfolio/positions', methods=['GET'])
def get_positions():
    """
    Get all positions across accounts.
    
    Query Parameters:
        account_hash (optional): Filter by specific account
        
    Returns:
        JSON: List of all portfolio positions
    """
    try:
        schwab_client = get_schwab_client()
        account_hash = request.args.get('account_hash')
        
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        # Get portfolio data with positions
        portfolio_data = schwab_client.get_portfolio_data(account_hash=account_hash)
        
        # Extract positions from the response
        positions = []
        if isinstance(portfolio_data, list):
            for account in portfolio_data:
                securities_account = account.get('securitiesAccount', {})
                account_positions = securities_account.get('positions', [])
                positions.extend(account_positions)
        else:
            securities_account = portfolio_data.get('securitiesAccount', {})
            positions = securities_account.get('positions', [])
        
        return jsonify({
            'success': True,
            'data': {
                'positions': positions,
                'count': len(positions)
            }
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


@api_bp.route('/portfolio/summary', methods=['GET'])
def get_portfolio_summary():
    """
    Get portfolio summary including total value, positions count, etc.
    
    Query Parameters:
        account_hash (optional): Filter by specific account
        
    Returns:
        JSON: Portfolio summary statistics
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
        
        # Calculate summary statistics
        summary = {
            'total_accounts': 0,
            'total_positions': 0,
            'total_value': 0.0,
            'total_cash': 0.0
        }
        
        if isinstance(portfolio_data, list):
            summary['total_accounts'] = len(portfolio_data)
            for account in portfolio_data:
                securities_account = account.get('securitiesAccount', {})
                positions = securities_account.get('positions', [])
                summary['total_positions'] += len(positions)
                
                # Sum up position values
                for position in positions:
                    market_value = position.get('marketValue', 0)
                    summary['total_value'] += market_value
                
                # Add cash balances
                balances = securities_account.get('currentBalances', {})
                cash = balances.get('cashBalance', 0)
                summary['total_cash'] += cash
        else:
            summary['total_accounts'] = 1
            securities_account = portfolio_data.get('securitiesAccount', {})
            positions = securities_account.get('positions', [])
            summary['total_positions'] = len(positions)
            
            for position in positions:
                market_value = position.get('marketValue', 0)
                summary['total_value'] += market_value
            
            balances = securities_account.get('currentBalances', {})
            summary['total_cash'] = balances.get('cashBalance', 0)
        
        summary['total_value'] += summary['total_cash']
        
        return jsonify({
            'success': True,
            'data': summary
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
