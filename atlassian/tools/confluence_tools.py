"""Business logic for Confluence tools."""

import json
import logging
from typing import Dict, Any, List, Optional

from ..clients.confluence_client import ConfluenceClient
from ..auth.config import ConfluenceConfig
from ..utils.exceptions import AtlassianError, AuthenticationError, APIError

logger = logging.getLogger(__name__)


class ConfluenceTools:
    """Business logic for Confluence operations."""
    
    def __init__(self):
        self._client = None
    
    def _get_client(self) -> ConfluenceClient:
        """Get or create Confluence client."""
        if self._client is None:
            config = ConfluenceConfig.from_env()
            if not config.is_auth_configured():
                raise AuthenticationError("Confluence authentication not configured. Please set CONFLUENCE_URL and authentication credentials.")
            self._client = ConfluenceClient(config)
        return self._client
    
    def search(self, query: str, limit: int = 25, start: int = 0) -> str:
        """Search Confluence content using CQL."""
        try:
            client = self._get_client()
            
            # Convert simple queries to CQL if needed
            if query and not any(x in query for x in ["=", "~", ">", "<", " AND ", " OR "]):
                cql_query = f'siteSearch ~ "{query}"'
            else:
                cql_query = query
            
            search_result = client.search_content(cql_query, limit=limit, start=start)
            
            # Extract and simplify results
            results = search_result.get('results', [])
            simplified_results = []
            for result in results:
                simplified_results.append({
                    'id': result.get('id'),
                    'title': result.get('title'),
                    'type': result.get('type'),
                    'space': result.get('space', {}).get('name'),
                    'spaceKey': result.get('space', {}).get('key'),
                    'url': result.get('_links', {}).get('webui')
                })
            
            return json.dumps(simplified_results, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error searching Confluence with query '{query}': {e}")
            return json.dumps({
                "error": f"Failed to search Confluence: {str(e)}",
                "query": query
            }, indent=2)
    
    def get_page(self, page_id: Optional[str] = None, title: Optional[str] = None, space_key: Optional[str] = None) -> str:
        """Get content of a specific Confluence page."""
        try:
            client = self._get_client()
            
            if page_id:
                page_data = client.get_page(page_id)
            elif title and space_key:
                page_data = client.get_page_by_title(space_key, title)
                if not page_data:
                    return json.dumps({
                        "error": f"Page with title '{title}' not found in space '{space_key}'"
                    }, indent=2)
            else:
                return json.dumps({
                    "error": "Either 'page_id' OR both 'title' and 'space_key' must be provided"
                }, indent=2)
            
            # Simplify page data
            simplified_page = {
                'id': page_data.get('id'),
                'title': page_data.get('title'),
                'type': page_data.get('type'),
                'space': page_data.get('space', {}).get('name'),
                'spaceKey': page_data.get('space', {}).get('key'),
                'content': page_data.get('body', {}).get('storage', {}).get('value', ''),
                'version': page_data.get('version', {}).get('number'),
                'url': page_data.get('_links', {}).get('webui')
            }
            
            return json.dumps({
                "metadata": simplified_page
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting Confluence page: {e}")
            return json.dumps({
                "error": f"Failed to get page: {str(e)}"
            }, indent=2)
    
    def create_page(self, space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> str:
        """Create a new Confluence page."""
        try:
            client = self._get_client()
            page_data = client.create_page(space_key, title, content, parent_id)
            
            simplified_page = {
                'id': page_data.get('id'),
                'title': page_data.get('title'),
                'type': page_data.get('type'),
                'space': page_data.get('space', {}).get('name'),
                'spaceKey': page_data.get('space', {}).get('key'),
                'version': page_data.get('version', {}).get('number'),
                'url': page_data.get('_links', {}).get('webui')
            }
            
            return json.dumps({
                "message": "Page created successfully",
                "page": simplified_page
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error creating Confluence page: {e}")
            return json.dumps({
                "error": f"Failed to create page: {str(e)}",
                "space_key": space_key,
                "title": title
            }, indent=2)
    
    def update_page(self, page_id: str, title: str, content: str, parent_id: Optional[str] = None) -> str:
        """Update an existing Confluence page."""
        try:
            client = self._get_client()
            
            # Get current page to get version number
            current_page = client.get_page(page_id)
            current_version = current_page.get('version', {}).get('number', 0)
            
            page_data = client.update_page(page_id, title, content, current_version, parent_id)
            
            simplified_page = {
                'id': page_data.get('id'),
                'title': page_data.get('title'),
                'type': page_data.get('type'),
                'space': page_data.get('space', {}).get('name'),
                'spaceKey': page_data.get('space', {}).get('key'),
                'version': page_data.get('version', {}).get('number'),
                'url': page_data.get('_links', {}).get('webui')
            }
            
            return json.dumps({
                "message": "Page updated successfully",
                "page": simplified_page
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error updating Confluence page {page_id}: {e}")
            return json.dumps({
                "error": f"Failed to update page {page_id}: {str(e)}",
                "page_id": page_id
            }, indent=2)
    
    def delete_page(self, page_id: str) -> str:
        """Delete a Confluence page."""
        try:
            client = self._get_client()
            success = client.delete_page(page_id)
            
            if success:
                return json.dumps({
                    "success": True,
                    "message": f"Page {page_id} deleted successfully"
                }, indent=2)
            else:
                return json.dumps({
                    "success": False,
                    "message": f"Unable to delete page {page_id}"
                }, indent=2)
                
        except Exception as e:
            logger.error(f"Error deleting Confluence page {page_id}: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "page_id": page_id
            }, indent=2)
    
    def add_comment(self, page_id: str, content: str) -> str:
        """Add a comment to a Confluence page."""
        try:
            client = self._get_client()
            comment_data = client.add_comment(page_id, content)
            
            simplified_comment = {
                'id': comment_data.get('id'),
                'type': comment_data.get('type'),
                'content': comment_data.get('body', {}).get('storage', {}).get('value', ''),
                'version': comment_data.get('version', {}).get('number'),
            }
            
            return json.dumps({
                "success": True,
                "message": "Comment added successfully",
                "comment": simplified_comment
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error adding comment to Confluence page {page_id}: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "page_id": page_id
            }, indent=2)
    
    def get_page_children(self, parent_id: str, limit: int = 25, start: int = 0) -> str:
        """Get child pages of a Confluence page."""
        try:
            client = self._get_client()
            children = client.get_page_children(parent_id, limit=limit, start=start)
            
            simplified_children = []
            for child in children:
                simplified_children.append({
                    'id': child.get('id'),
                    'title': child.get('title'),
                    'type': child.get('type'),
                    'space': child.get('space', {}).get('name'),
                    'spaceKey': child.get('space', {}).get('key'),
                    'url': child.get('_links', {}).get('webui')
                })
            
            return json.dumps({
                "parent_id": parent_id,
                "count": len(simplified_children),
                "results": simplified_children
            }, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting children for Confluence page {parent_id}: {e}")
            return json.dumps({
                "error": f"Failed to get child pages: {str(e)}",
                "parent_id": parent_id
            }, indent=2)
    
    def get_page_labels(self, page_id: str) -> str:
        """Get labels for a Confluence page."""
        try:
            client = self._get_client()
            labels = client.get_page_labels(page_id)
            return json.dumps(labels, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error getting labels for Confluence page {page_id}: {e}")
            return json.dumps({
                "error": f"Failed to get labels: {str(e)}",
                "page_id": page_id
            }, indent=2)
    
    def add_page_label(self, page_id: str, label_name: str) -> str:
        """Add a label to a Confluence page."""
        try:
            client = self._get_client()
            labels = client.add_page_label(page_id, label_name)
            return json.dumps(labels, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error adding label to Confluence page {page_id}: {e}")
            return json.dumps({
                "error": f"Failed to add label: {str(e)}",
                "page_id": page_id,
                "label_name": label_name
            }, indent=2)