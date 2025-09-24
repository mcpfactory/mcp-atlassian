"""Configuration classes for Jira and Confluence authentication."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class JiraConfig:
    """Configuration for Jira connection."""
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    cloud_id: Optional[str] = None
    oauth_token: Optional[str] = None
    projects_filter: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "JiraConfig":
        """Create config from environment variables."""
        return cls(
            url=os.environ.get("JIRA_URL", ""),
            username=os.environ.get("ATLASSIAN_USERNAME"),
            password=os.environ.get("ATLASSIAN_PASSWORD"),
            token=os.environ.get("ATLASSIAN_API_TOKEN"),
            cloud_id=os.environ.get("ATLASSIAN_CLOUD_ID"),
            oauth_token=os.environ.get("ATLASSIAN_OAUTH_TOKEN"),
            projects_filter=os.environ.get("JIRA_PROJECTS_FILTER"),
        )
    
    def is_auth_configured(self) -> bool:
        """Check if authentication is properly configured."""
        return bool(self.url and (
            (self.username and self.password) or 
            (self.username and self.token) or
            self.oauth_token
        ))
    
    @property
    def is_cloud(self) -> bool:
        """Check if this is a Jira Cloud instance."""
        return "atlassian.net" in self.url if self.url else False


@dataclass
class ConfluenceConfig:
    """Configuration for Confluence connection."""
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    cloud_id: Optional[str] = None
    oauth_token: Optional[str] = None
    spaces_filter: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "ConfluenceConfig":
        """Create config from environment variables."""
        return cls(
            url=os.environ.get("CONFLUENCE_URL", ""),
            username=os.environ.get("ATLASSIAN_USERNAME"),
            password=os.environ.get("ATLASSIAN_PASSWORD"),
            token=os.environ.get("ATLASSIAN_API_TOKEN"),
            cloud_id=os.environ.get("ATLASSIAN_CLOUD_ID"),
            oauth_token=os.environ.get("CONFLUENCE_OAUTH_TOKEN"),
            spaces_filter=os.environ.get("CONFLUENCE_SPACES_FILTER"),
        )
    
    def is_auth_configured(self) -> bool:
        """Check if authentication is properly configured."""
        return bool(self.url and (
            (self.username and self.password) or 
            (self.username and self.token) or
            self.oauth_token
        ))
    
    @property
    def is_cloud(self) -> bool:
        """Check if this is a Confluence Cloud instance."""
        return "atlassian.net" in self.url if self.url else False