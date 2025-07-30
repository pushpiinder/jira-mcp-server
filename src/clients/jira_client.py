"""
JIRA Client for MCP Server
Using direct REST API calls with API token authentication
"""

import asyncio
import json
import logging
import aiohttp
import base64
from typing import Dict, Optional, List, Any

logger = logging.getLogger(__name__)

class JiraClient:
    """JIRA API client using direct REST API calls"""
    
    def __init__(self, base_url: str, api_token: str, cloud_id: str, username: str = None):
        self.base_url = base_url
        self.api_token = api_token
        self.cloud_id = cloud_id
        self.username = username
        self.session = None
        
        # Create basic auth header
        if username:
            auth_string = f"{username}:{api_token}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            self.headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        else:
            # Use Bearer token (for API tokens)
            self.headers = {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self.session
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Optional[Dict]:
        """Make HTTP request to JIRA API"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/rest/api/3/{endpoint}"
            
            async with session.request(method, url, json=data) as response:
                if response.status in [200, 201, 204]:  # 204 is success for updates
                    if response.status == 204:  # No content for updates
                        return {"success": True}
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"API request failed: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    async def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Optional[str]:
        """Create JIRA issue using REST API"""
        try:
            data = {
                "fields": {
                    "project": {
                        "key": project_key
                    },
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": description
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {
                        "name": issue_type
                    }
                }
            }
            
            result = await self._make_request("POST", "issue", data)
            
            if result and "key" in result:
                logger.info(f"✅ Issue created: {result['key']}")
                return result["key"]
            else:
                logger.error("❌ Failed to create issue")
                return None
                
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return None
    
    async def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search JIRA issues using REST API"""
        try:
            data = {
                "jql": jql,
                "maxResults": max_results,
                "fields": ["summary", "status", "assignee", "created", "updated"]
            }
            
            result = await self._make_request("POST", "search", data)
            
            if result and "issues" in result:
                return result["issues"]
            return []
            
        except Exception as e:
            logger.error(f"Error searching issues: {e}")
            return []
    
    async def get_projects(self) -> List[Dict]:
        """Get visible JIRA projects using REST API"""
        try:
            result = await self._make_request("GET", "project")
            
            if result:
                return result
            return []
            
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return []
    
    async def update_issue(self, issue_key: str, fields: Dict[str, Any]) -> bool:
        """Update JIRA issue using REST API"""
        try:
            data = {"fields": fields}
            
            result = await self._make_request("PUT", f"issue/{issue_key}", data)
            
            if result is not None:
                logger.info(f"✅ Issue updated: {issue_key}")
                return True
            else:
                logger.error(f"❌ Failed to update issue: {issue_key}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating issue: {e}")
            return False
    
    async def close(self):
        """Close HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close() 