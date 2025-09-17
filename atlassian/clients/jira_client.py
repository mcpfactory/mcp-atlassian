"""Jira client for API interactions."""

import json
import logging
from typing import Dict, Any, List, Optional

from .base_client import BaseAtlassianClient
from ..auth.config import JiraConfig
from ..utils.exceptions import APIError

logger = logging.getLogger(__name__)


class JiraClient(BaseAtlassianClient):
    """Client for Jira API interactions."""
    
    def __init__(self, config: JiraConfig):
        super().__init__(config)
        self.api_base = "rest/api/3" if config.is_cloud else "rest/api/2"
    
    def get_issue(self, issue_key: str, fields: Optional[List[str]] = None, expand: Optional[str] = None) -> Dict[str, Any]:
        """Get a Jira issue by key."""
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        if expand:
            params['expand'] = expand
        
        return self.get(f"{self.api_base}/issue/{issue_key}", params=params)
    
    def search_issues(self, jql: str, fields: Optional[List[str]] = None, start_at: int = 0, max_results: int = 50) -> Dict[str, Any]:
        """Search issues using JQL."""
        data = {
            'jql': jql,
            'startAt': start_at,
            'maxResults': max_results
        }
        if fields:
            data['fields'] = fields
        
        return self.post(f"{self.api_base}/search", json_data=data)
    
    def create_issue(self, project_key: str, summary: str, issue_type: str, **kwargs) -> Dict[str, Any]:
        """Create a new Jira issue."""
        fields = {
            'project': {'key': project_key},
            'summary': summary,
            'issuetype': {'name': issue_type}
        }
        
        # Add optional fields
        if 'description' in kwargs:
            fields['description'] = {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': kwargs['description']
                            }
                        ]
                    }
                ]
            }
        
        if 'assignee' in kwargs:
            if self.config.is_cloud:
                fields['assignee'] = {'id': kwargs['assignee']}
            else:
                fields['assignee'] = {'name': kwargs['assignee']}
        
        data = {'fields': fields}
        return self.post(f"{self.api_base}/issue", json_data=data)
    
    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update a Jira issue."""
        data = {'fields': fields}
        return self.put(f"{self.api_base}/issue/{issue_key}", json_data=data)
    
    def delete_issue(self, issue_key: str) -> bool:
        """Delete a Jira issue."""
        try:
            self.delete(f"{self.api_base}/issue/{issue_key}")
            return True
        except APIError:
            return False
    
    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """Add a comment to an issue."""
        data = {
            'body': {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': comment
                            }
                        ]
                    }
                ]
            }
        }
        return self.post(f"{self.api_base}/issue/{issue_key}/comment", json_data=data)
    
    def get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available transitions for an issue."""
        result = self.get(f"{self.api_base}/issue/{issue_key}/transitions")
        return result.get('transitions', [])
    
    def transition_issue(self, issue_key: str, transition_id: str, fields: Optional[Dict] = None, comment: Optional[str] = None) -> Dict[str, Any]:
        """Transition an issue to a new status."""
        data = {
            'transition': {'id': transition_id}
        }
        if fields:
            data['fields'] = fields
        if comment:
            data['update'] = {
                'comment': [{
                    'add': {
                        'body': {
                            'type': 'doc',
                            'version': 1,
                            'content': [
                                {
                                    'type': 'paragraph',
                                    'content': [
                                        {
                                            'type': 'text',
                                            'text': comment
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }]
            }
        
        return self.post(f"{self.api_base}/issue/{issue_key}/transitions", json_data=data)
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all accessible projects."""
        result = self.get(f"{self.api_base}/project")
        return result if isinstance(result, list) else []
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user information."""
        if self.config.is_cloud:
            return self.get(f"{self.api_base}/user", params={'accountId': user_id})
        else:
            return self.get(f"{self.api_base}/user", params={'username': user_id})