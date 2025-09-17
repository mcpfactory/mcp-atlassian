"""Business logic for Jira tools."""

import json
import logging
from typing import Dict, Any, List, Optional

from ..clients.jira_client import JiraClient
from ..auth.config import JiraConfig
from ..utils.exceptions import AtlassianError, AuthenticationError, APIError

logger = logging.getLogger(__name__)


class JiraTools:
    """Business logic for Jira operations."""
    
    def __init__(self):
        self._client = None
    
    def _get_client(self) -> JiraClient:
        """Get or create Jira client."""
        if self._client is None:
            config = JiraConfig.from_env()
            if not config.is_auth_configured():
                raise AuthenticationError("Jira authentication not configured. Please set JIRA_URL and authentication credentials.")
            self._client = JiraClient(config)
        return self._client
    
    def get_issue(self, issue_key: str, fields: Optional[str] = None, expand: Optional[str] = None) -> str:
        """Get details of a specific Jira issue."""
        try:
            client = self._get_client()
            field_list = fields.split(',') if fields and fields != '*all' else None
            
            issue_data = client.get_issue(issue_key, fields=field_list, expand=expand)
            return json.dumps(issue_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to get issue {issue_key}: {str(e)}",
                "issue_key": issue_key
            }, indent=2)
    
    def search_issues(self, jql: str, fields: Optional[str] = None, start_at: int = 0, max_results: int = 50) -> str:
        """Search Jira issues using JQL."""
        try:
            client = self._get_client()
            field_list = fields.split(',') if fields and fields != '*all' else None
            
            search_result = client.search_issues(jql, fields=field_list, start_at=start_at, max_results=max_results)
            return json.dumps(search_result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error searching issues with JQL '{jql}': {e}")
            return json.dumps({
                "error": f"Failed to search issues: {str(e)}",
                "jql": jql
            }, indent=2)
    
    def create_issue(self, project_key: str, summary: str, issue_type: str, description: Optional[str] = None, assignee: Optional[str] = None) -> str:
        """Create a new Jira issue."""
        try:
            client = self._get_client()
            kwargs = {}
            if description:
                kwargs['description'] = description
            if assignee:
                kwargs['assignee'] = assignee
            
            issue_data = client.create_issue(project_key, summary, issue_type, **kwargs)
            return json.dumps({
                "message": "Issue created successfully",
                "issue": issue_data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return json.dumps({
                "error": f"Failed to create issue: {str(e)}",
                "project_key": project_key,
                "summary": summary
            }, indent=2)
    
    def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> str:
        """Update an existing Jira issue."""
        try:
            client = self._get_client()
            client.update_issue(issue_key, fields)
            
            # Get updated issue
            updated_issue = client.get_issue(issue_key)
            return json.dumps({
                "message": "Issue updated successfully",
                "issue": updated_issue
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error updating issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to update issue {issue_key}: {str(e)}",
                "issue_key": issue_key
            }, indent=2)
    
    def delete_issue(self, issue_key: str) -> str:
        """Delete a Jira issue."""
        try:
            client = self._get_client()
            success = client.delete_issue(issue_key)
            
            if success:
                return json.dumps({
                    "message": f"Issue {issue_key} has been deleted successfully."
                }, indent=2)
            else:
                return json.dumps({
                    "error": f"Failed to delete issue {issue_key}. Issue may not exist or you may not have permission."
                }, indent=2)
                
        except Exception as e:
            logger.error(f"Error deleting issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to delete issue {issue_key}: {str(e)}",
                "issue_key": issue_key
            }, indent=2)
    
    def add_comment(self, issue_key: str, comment: str) -> str:
        """Add a comment to a Jira issue."""
        try:
            client = self._get_client()
            comment_data = client.add_comment(issue_key, comment)
            return json.dumps({
                "message": "Comment added successfully",
                "comment": comment_data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error adding comment to issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to add comment to issue {issue_key}: {str(e)}",
                "issue_key": issue_key
            }, indent=2)
    
    def get_transitions(self, issue_key: str) -> str:
        """Get available transitions for a Jira issue."""
        try:
            client = self._get_client()
            transitions = client.get_transitions(issue_key)
            return json.dumps(transitions, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting transitions for issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to get transitions for issue {issue_key}: {str(e)}",
                "issue_key": issue_key
            }, indent=2)
    
    def transition_issue(self, issue_key: str, transition_id: str, fields: Optional[Dict[str, Any]] = None, comment: Optional[str] = None) -> str:
        """Transition a Jira issue to a new status."""
        try:
            client = self._get_client()
            client.transition_issue(issue_key, transition_id, fields, comment)
            
            # Get updated issue
            updated_issue = client.get_issue(issue_key)
            return json.dumps({
                "message": f"Issue {issue_key} transitioned successfully",
                "issue": updated_issue
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error transitioning issue {issue_key}: {e}")
            return json.dumps({
                "error": f"Failed to transition issue {issue_key}: {str(e)}",
                "issue_key": issue_key,
                "transition_id": transition_id
            }, indent=2)
    
    def get_projects(self) -> str:
        """Get all accessible Jira projects."""
        try:
            client = self._get_client()
            projects = client.get_projects()
            return json.dumps(projects, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return json.dumps({
                "error": f"Failed to get projects: {str(e)}"
            }, indent=2)
    
    def get_user_profile(self, user_identifier: str) -> str:
        """Get Jira user profile information."""
        try:
            client = self._get_client()
            user_data = client.get_user(user_identifier)
            return json.dumps({
                "success": True,
                "user": user_data
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting user profile for '{user_identifier}': {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "user_identifier": user_identifier
            }, indent=2)