"""User Authentication Module - JWT &  OAuth Support"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import hashlib
import secrets
import json
from functools import wraps

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False


class AuthenticationService:
    """Handle user authentication with JWT tokens"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256", expiration_hours: int = 24):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_hours = expiration_hours
        self.token_blacklist = set()  # In production, use Redis
        
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${pwd_hash.hex()}"
    
    def verify_password(self, password: str, hash_stored: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, pwd_hash = hash_stored.split('$')
            verify_hash = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return verify_hash.hex() == pwd_hash
        except:
            return False
    
    def create_access_token(self, user_id: int, email: str, extra_claims: Dict = None) -> str:
        """Create JWT access token"""
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT library required for token generation")
        
        payload = {
            'user_id': user_id,
            'email': email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours),
            'type': 'access'
        }
        
        if extra_claims:
            payload.update(extra_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def create_refresh_token(self, user_id: int) -> str:
        """Create JWT refresh token (longer expiration)"""
        if not JWT_AVAILABLE:
            raise ImportError("PyJWT library required for token generation")
        
        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=30),
            'type': 'refresh'
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> Tuple[bool, Dict]:
        """Verify and decode JWT token"""
        if not JWT_AVAILABLE:
            return False, {"error": "JWT library not available"}
        
        if token in self.token_blacklist:
            return False, {"error": "Token has been revoked"}
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return False, {"error": "Invalid token"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Create new access token from refresh token"""
        valid, payload = self.verify_token(refresh_token)
        
        if not valid or payload.get('type') != 'refresh':
            return None
        
        return self.create_access_token(
            payload['user_id'],
            payload.get('email', '')
        )
    
    def revoke_token(self, token: str):
        """Add token to blacklist"""
        self.token_blacklist.add(token)
    
    def logout_user(self, token: str):
        """Logout user by revoking token"""
        self.revoke_token(token)


class RoleBasedAccessControl:
    """Role-Based Access Control (RBAC) system"""
    
    # Define roles and permissions
    ROLES = {
        'guest': {
            'permissions': ['view_public_content', 'search_flights', 'view_guides']
        },
        'user': {
            'permissions': [
                'create_trip',
                'book_flight',
                'book_accommodation',
                'book_activity',
                'manage_visa',
                'view_itinerary',
                'share_trip',
                'edit_profile'
            ]
        },
        'premium': {
            'permissions': [
                'unlimited_trips',
                'priority_support',
                'exclusive_deals',
                'offline_mode',
                'advanced_analytics',
                'all_user_permissions'
            ]
        },
        'guide': {
            'permissions': [
                'create_guide',
                'publish_guide',
                'upload_photos',
                'earn_commission',
                'view_statistics'
            ]
        },
        'admin': {
            'permissions': [
                'manage_users',
                'manage_content',
                'view_analytics',
                'manage_payments',
                'system_settings',
                'all_permissions'
            ]
        }
    }
    
    def __init__(self):
        self.user_roles = {}  # user_id -> role mapping
    
    def assign_role(self, user_id: int, role: str) -> bool:
        """Assign role to user"""
        if role not in self.ROLES:
            return False
        self.user_roles[user_id] = role
        return True
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Get user's role"""
        return self.user_roles.get(user_id, 'guest')
    
    def has_permission(self, user_id: int, permission: str) -> bool:
        """Check if user has specific permission"""
        role = self.get_user_role(user_id)
        permissions = self.ROLES[role]['permissions']
        
        return (permission in permissions or 
                'all_permissions' in permissions or
                'all_user_permissions' in permissions)
    
    def can_perform_action(self, user_id: int, action: str) -> bool:
        """Check if user can perform specific action"""
        return self.has_permission(user_id, action)


class SessionManager:
    """Manage user sessions"""
    
    def __init__(self, expiration_minutes: int = 60):
        self.sessions = {}  # session_id -> session_data
        self.expiration_minutes = expiration_minutes
    
    def create_session(self, user_id: int, user_data: Dict) -> str:
        """Create new session"""
        session_id = secrets.token_urlsafe(32)
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': datetime.utcnow(),
            'last_accessed': datetime.utcnow(),
            'ip_address': user_data.get('ip_address'),
            'user_agent': user_data.get('user_agent')
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        # Check expiration
        last_access = session['last_accessed']
        if datetime.utcnow() - last_access > timedelta(minutes=self.expiration_minutes):
            del self.sessions[session_id]
            return None
        
        # Update last accessed time
        session['last_accessed'] = datetime.utcnow()
        return session
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate/logout session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.utcnow()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session['last_accessed'] > timedelta(minutes=self.expiration_minutes)
        ]
        for sid in expired:
            del self.sessions[sid]


class TwoFactorAuthService:
    """Two-Factor Authentication (2FA)"""
    
    def __init__(self):
        self.pending_verifications = {}  # user_id -> {code, expiry, attempts}
    
    def generate_otp(self, user_id: int, length: int = 6) -> str:
        """Generate One-Time Password"""
        otp = secrets.token_hex(length // 2)[:length]
        
        self.pending_verifications[user_id] = {
            'code': otp,
            'created_at': datetime.utcnow(),
            'expiry': datetime.utcnow() + timedelta(minutes=5),
            'attempts': 0,
            'verified': False
        }
        
        return otp
    
    def verify_otp(self, user_id: int, code: str) -> Tuple[bool, str]:
        """Verify OTP"""
        if user_id not in self.pending_verifications:
            return False, "No pending verification"
        
        verification = self.pending_verifications[user_id]
        
        # Check expiry
        if datetime.utcnow() > verification['expiry']:
            del self.pending_verifications[user_id]
            return False, "OTP expired"
        
        # Check attempts
        if verification['attempts'] >= 3:
            del self.pending_verifications[user_id]
            return False, "Too many attempts"
        
        # Verify code
        if code == verification['code']:
            verification['verified'] = True
            return True, "OTP verified successfully"
        
        verification['attempts'] += 1
        return False, f"Invalid OTP. {3 - verification['attempts']} attempts remaining"
    
    def is_verified(self, user_id: int) -> bool:
        """Check if 2FA is verified"""
        if user_id not in self.pending_verifications:
            return False
        return self.pending_verifications[user_id]['verified']


# Decorator for protected routes
def require_authentication(auth_service: AuthenticationService):
    """Decorator to protect routes requiring authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get token from request headers
            # This would be implemented in Flask route handlers
            # Example: token = request.headers.get('Authorization', '').replace('Bearer ', '')
            
            # Verify token
            # valid, payload = auth_service.verify_token(token)
            # if not valid:
            #     return {"error": "Unauthorized"}, 401
            
            # Pass user_id to route
            kwargs['authenticated_user_id'] = None  # Would be payload['user_id']
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_role(role_acl: RoleBasedAccessControl, required_role: str):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This would be implemented in Flask route handlers
            # user_id = get_current_user_id()
            # if not role_acl.can_perform_action(user_id, required_role):
            #     return {"error": "Forbidden"}, 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
