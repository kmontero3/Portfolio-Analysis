"""
Authentication Routes for Schwab API

Handles OAuth authentication and token management.
"""

from flask import jsonify, current_app
from app.blueprints.api import api_bp
from app.blueprints.api.schwab_integration import SchwabClient, SchwabAPIError


def get_schwab_client():
    """
    Get or create a SchwabClient instance using app configuration.
    
    Returns:
        SchwabClient: Configured Schwab API client instance
    """
    if not hasattr(current_app, 'schwab_client'):
        from config import Config
        current_app.schwab_client = SchwabClient(
            api_key=Config.SCHWAB_API_KEY,
            api_secret=Config.SCHWAB_API_SECRET,
            redirect_uri=Config.SCHWAB_REDIRECT_URI
        )
    return current_app.schwab_client


@api_bp.route('/auth/status', methods=['GET'])
def auth_status():
    """
    Check authentication status.
    
    Returns:
        JSON: Authentication status information including token validity,
              expiration time, and available scopes
    """
    try:
        schwab_client = get_schwab_client()
        status = schwab_client.test_connectivity()
        
        return jsonify({
            'success': True,
            'data': status
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Error',
            'message': str(e)
        }), 500


@api_bp.route('/auth/url', methods=['GET'])
def get_auth_url():
    """
    Get OAuth authorization URL.
    
    Returns:
        JSON: Authorization URL for user to visit to authenticate
    """
    try:
        schwab_client = get_schwab_client()
        auth_url = schwab_client.get_authorization_url()
        
        return jsonify({
            'success': True,
            'data': {
                'authorization_url': auth_url
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal Error',
            'message': str(e)
        }), 500


@api_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """
    Get all account numbers for the authenticated user.
    
    Returns:
        JSON: List of account information with account hashes
    """
    try:
        schwab_client = get_schwab_client()
        
        # Ensure client is authenticated
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        accounts = schwab_client.get_account_numbers()
        return jsonify({
            'success': True,
            'data': accounts
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


@api_bp.route('/account/<account_hash>', methods=['GET'])
def get_account(account_hash):
    """
    Get specific account data.
    
    Args:
        account_hash: Account hash identifier
        
    Query Parameters:
        fields (optional): Fields to include (e.g., 'positions')
        
    Returns:
        JSON: Account data including balances and optionally positions
    """
    try:
        from flask import request
        schwab_client = get_schwab_client()
        
        # Ensure client is authenticated
        if not schwab_client.access_token:
            return jsonify({
                'error': 'Not authenticated',
                'message': 'Please authenticate with Schwab API first'
            }), 401
        
        fields = request.args.get('fields', 'positions')
        account_data = schwab_client.get_account_data(
            account_hash=account_hash,
            fields=fields
        )
        
        return jsonify({
            'success': True,
            'data': account_data
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
