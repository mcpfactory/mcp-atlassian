"""Base client for Atlassian services."""

import json
import logging
from typing import Dict, Any, Optional
import requests
from requests.auth import HTTPBasicAuth

from ..auth.config import JiraConfig, ConfluenceConfig
from ..utils.exceptions import AuthenticationError, APIError

logger = logging.getLogger(__name__)


class BaseAtlassianClient:
    """Base client for Atlassian API interactions."""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication for the session."""
        if self.config.oauth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.config.oauth_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
        elif self.config.username and (self.config.password or self.config.token):
            password = self.config.token or self.config.password
            self.session.auth = HTTPBasicAuth(self.config.username, password)
            self.session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
        else:
            raise AuthenticationError("No valid authentication method configured")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to the API."""
        url = f"{self.config.url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError(f"Authentication failed: {e}")
            elif response.status_code == 403:
                raise AuthenticationError(f"Access denied: {e}")
            else:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                raise APIError(
                    f"API request failed: {e}", 
                    status_code=response.status_code,
                    response_data=error_data
                )
        except requests.exceptions.RequestException as e:
            raise APIError(f"Network error: {e}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a POST request."""
        kwargs = {}
        if json_data:
            kwargs['json'] = json_data
        if data:
            kwargs['data'] = data
        return self._make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        kwargs = {}
        if json_data:
            kwargs['json'] = json_data
        if data:
            kwargs['data'] = data
        return self._make_request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request('DELETE', endpoint)