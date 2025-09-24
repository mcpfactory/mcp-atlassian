"""Confluence client for API interactions."""

import json
import logging
from typing import Dict, Any, List, Optional

from .base_client import BaseAtlassianClient
from ..auth.config import ConfluenceConfig
from ..utils.exceptions import APIError

logger = logging.getLogger(__name__)


class ConfluenceClient(BaseAtlassianClient):
    """Client for Confluence API interactions."""
    
    def __init__(self, config: ConfluenceConfig):
        super().__init__(config)
        self.api_base = "rest/api"
    
    def search_content(self, cql: str, limit: int = 25, start: int = 0) -> Dict[str, Any]:
        """Search Confluence content using CQL."""
        params = {
            'cql': cql,
            'limit': limit,
            'start': start,
            'expand': 'version,space,body.storage'
        }
        return self.get(f"{self.api_base}/search", params=params)
    
    def get_page(self, page_id: str, expand: Optional[str] = None) -> Dict[str, Any]:
        """Get a Confluence page by ID."""
        params = {}
        if expand:
            params['expand'] = expand
        else:
            params['expand'] = 'body.storage,version,space'
        
        return self.get(f"{self.api_base}/content/{page_id}", params=params)
    
    def get_page_by_title(self, space_key: str, title: str) -> Optional[Dict[str, Any]]:
        """Get a page by title and space key."""
        params = {
            'spaceKey': space_key,
            'title': title,
            'expand': 'body.storage,version,space'
        }
        result = self.get(f"{self.api_base}/content", params=params)
        results = result.get('results', [])
        return results[0] if results else None
    
    def get_page_children(self, page_id: str, limit: int = 25, start: int = 0, expand: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get child pages of a page."""
        params = {
            'limit': limit,
            'start': start
        }
        if expand:
            params['expand'] = expand
        else:
            params['expand'] = 'version,space'
        
        result = self.get(f"{self.api_base}/content/{page_id}/child/page", params=params)
        return result.get('results', [])
    
    def create_page(self, space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Confluence page."""
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': space_key},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        
        if parent_id:
            data['ancestors'] = [{'id': parent_id}]
        
        return self.post(f"{self.api_base}/content", json_data=data)
    
    def update_page(self, page_id: str, title: str, content: str, version: int, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing Confluence page."""
        data = {
            'id': page_id,
            'type': 'page',
            'title': title,
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            },
            'version': {'number': version + 1}
        }
        
        if parent_id:
            data['ancestors'] = [{'id': parent_id}]
        
        return self.put(f"{self.api_base}/content/{page_id}", json_data=data)
    
    def delete_page(self, page_id: str) -> bool:
        """Delete a Confluence page."""
        try:
            self.delete(f"{self.api_base}/content/{page_id}")
            return True
        except APIError:
            return False
    
    def get_page_comments(self, page_id: str) -> List[Dict[str, Any]]:
        """Get comments for a page."""
        result = self.get(f"{self.api_base}/content/{page_id}/child/comment", 
                         params={'expand': 'body.storage,version'})
        return result.get('results', [])
    
    def add_comment(self, page_id: str, content: str) -> Dict[str, Any]:
        """Add a comment to a page."""
        data = {
            'type': 'comment',
            'container': {'id': page_id},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }
        return self.post(f"{self.api_base}/content", json_data=data)
    
    def get_page_labels(self, page_id: str) -> List[Dict[str, Any]]:
        """Get labels for a page."""
        result = self.get(f"{self.api_base}/content/{page_id}/label")
        return result.get('results', [])
    
    def add_page_label(self, page_id: str, label_name: str) -> List[Dict[str, Any]]:
        """Add a label to a page."""
        data = [{'prefix': 'global', 'name': label_name}]
        self.post(f"{self.api_base}/content/{page_id}/label", json_data=data)
        return self.get_page_labels(page_id)