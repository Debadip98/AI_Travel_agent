"""Gmail OAuth authentication routes"""
from flask import Blueprint, request, jsonify, session, url_for, redirect
from functools import wraps
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import json
import os


# Gmail OAuth Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Configuration
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email'
]


def get_oauth_flow(config):
    """Create OAuth 2.0 flow"""
    try:
        return Flow.from_client_config(
            {
                "installed": {
                    "client_id": config.GMAIL_CLIENT_ID,
                    "client_secret": config.GMAIL_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [config.GMAIL_CALLBACK_URL]
                }
            },
            scopes=SCOPES
        )
    except Exception as e:
        print(f"OAuth flow error: {e}")
        return None


def require_gmail_auth(f):
    """Decorator to check if user is Gmail authenticated"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        gmail_token = session.get('gmail_token')
        if not gmail_token:
            return jsonify({"error": "Gmail authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function


def register_auth_routes(app):
    """Register authentication routes to Flask app"""
    
    @auth_bp.route('/gmail/start')
    def gmail_auth_start():
        """Start Gmail OAuth flow"""
        config = app.config
        flow = get_oauth_flow(config)
        
        if not flow:
            return jsonify({"error": "OAuth configuration error"}), 500
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        session['oauth_state'] = state
        return jsonify({
            "status": "success",
            "authorization_url": authorization_url
        })
    
    @auth_bp.route('/gmail/callback')
    def gmail_auth_callback():
        """Gmail OAuth callback"""
        config = app.config
        state = session.get('oauth_state')
        
        if not state:
            return jsonify({"error": "Missing state parameter"}), 400
        
        flow = get_oauth_flow(config)
        if not flow:
            return jsonify({"error": "OAuth configuration error"}), 500
        
        try:
            code = request.args.get('code')
            if not code:
                return jsonify({"error": "Missing authorization code"}), 400
            
            # Exchange code for token
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            # Store token in session
            session['gmail_token'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            
            # Redirect to frontend
            frontend_url = config.FRONTEND_URL or 'http://localhost:3000'
            return redirect(f"{frontend_url}?auth=success")
            
        except Exception as e:
            print(f"OAuth callback error: {e}")
            return jsonify({"error": str(e)}), 400
    
    @auth_bp.route('/gmail/status')
    def gmail_auth_status():
        """Check Gmail authentication status"""
        is_authenticated = 'gmail_token' in session
        return jsonify({
            "authenticated": is_authenticated,
            "status": "authenticated" if is_authenticated else "not_authenticated"
        })
    
    @auth_bp.route('/gmail/logout')
    def gmail_logout():
        """Logout from Gmail"""
        session.pop('gmail_token', None)
        return jsonify({
            "status": "success",
            "message": "Logged out from Gmail"
        })
    
    @auth_bp.route('/gmail/refresh-token', methods=['POST'])
    def gmail_refresh_token():
        """Refresh Gmail token"""
        token_data = session.get('gmail_token')
        if not token_data:
            return jsonify({"error": "Not authenticated"}), 401
        
        try:
            credentials = Credentials(
                token=token_data['token'],
                refresh_token=token_data['refresh_token'],
                token_uri=token_data['token_uri'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                scopes=token_data['scopes']
            )
            
            if credentials.expired and credentials.refresh_token:
                request_obj = google.auth.transport.requests.Request()
                credentials.refresh(request_obj)
                
                # Update session
                session['gmail_token'] = {
                    'token': credentials.token,
                    'refresh_token': credentials.refresh_token,
                    'token_uri': credentials.token_uri,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'scopes': credentials.scopes
                }
                session.modified = True
            
            return jsonify({
                "status": "success",
                "message": "Token refreshed"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @auth_bp.route('/gmail/send-email', methods=['POST'])
    @require_gmail_auth
    def send_gmail_email():
        """Send email via Gmail"""
        from integrations.gmail import gmail_manager
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        data = request.json
        token_data = session.get('gmail_token')
        
        try:
            # Create credentials from session
            credentials = Credentials(
                token=token_data['token'],
                refresh_token=token_data['refresh_token'],
                token_uri=token_data['token_uri'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                scopes=token_data['scopes']
            )
            
            # Refresh if needed
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            
            # Build Gmail service
            service = build('gmail', 'v1', credentials=credentials)
            
            # Send email
            result = gmail_manager.send_email(
                service=service,
                sender=data.get('to'),  # User's email
                to=data.get('to'),
                subject=data.get('subject'),
                body=data.get('body')
            )
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 400
    
    app.register_blueprint(auth_bp)
    return auth_bp
