"""Gmail OAuth and email integration"""
import os
from typing import Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import base64
from email.mime.text import MIMEText
from google.auth.exceptions import RefreshError


class GmailManager:
    """Manage Gmail API authentication and email sending"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.send', 
              'https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path or "credentials.json"
        self.service = None
    
    def authenticate(self, redirect_uri: str = None) -> str:
        """
        Start OAuth authentication flow
        
        Returns:
            Authorization URL for user to visit
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, self.SCOPES
        )
        
        if redirect_uri:
            flow.redirect_uri = redirect_uri
        
        auth_url, state = flow.authorization_url(prompt='consent')
        return auth_url
    
    def save_credentials(self, credentials: Credentials, save_path: str = "token.pickle"):
        """Save credentials for later use"""
        with open(save_path, 'wb') as token:
            pickle.dump(credentials, token)
    
    def load_credentials(self, token_path: str = "token.pickle") -> Credentials:
        """Load saved credentials"""
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
            # Refresh token if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            return creds
        return None
    
    def create_message(self, sender: str, to: str, subject: str, 
                       body: str) -> Dict[str, str]:
        """Create a message for sending"""
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    def send_email(self, service, sender: str, to: str, 
                   subject: str, body: str) -> Dict:
        """Send email through Gmail API"""
        try:
            message = self.create_message(sender, to, subject, body)
            result = service.users().messages().send(
                userId="me",
                body=message
            ).execute()
            
            return {
                "status": "success",
                "message_id": result.get('id'),
                "to": to,
                "subject": subject
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_profile(self, service) -> Dict:
        """Get user profile info"""
        try:
            profile = service.users().getProfile(userId='me').execute()
            return {
                "email": profile.get('emailAddress'),
                "messages_total": profile.get('messagesTotal'),
                "threads_total": profile.get('threadsTotal')
            }
        except Exception as e:
            return {"error": str(e)}


gmail_manager = GmailManager()
