"""
JIRA Search Tools for MCP Server
Using proven working patterns from WORKING_CODE_EXAMPLES.py
"""

import logging
from typing import List, Dict, Optional
from mcp.server.models import Tool
from clients.jira_client import JiraClient

logger = logging.getLogger(__name__)

class SearchIssuesTool(Tool):
    """Search JIRA issues using working pattern"""
    
    def __init__(self, jira_client: JiraClient):
        self.jira_client = jira_client
        super().__init__()
    
    name = "search_jira_issues"
    description = "Search JIRA issues using JQL with proven working patterns"
    
    async def run(
        self, 
        jql: str, 
        max_results: int = 50
    ) -> List[Dict]:
        """
        Search JIRA issues using the working pattern from examples
        
        Args:
            jql: JQL query string (e.g., 'created >= -7d ORDER BY created DESC')
            max_results: Maximum number of results to return
        
        Returns:
            List of issues matching the query
        """
        try:
            logger.info(f"Searching issues with JQL: {jql}")
            
            # Use the working pattern from examples
            issues = await self.jira_client.search_issues(
                jql=jql,
                max_results=max_results
            )
            
            logger.info(f"✅ Found {len(issues)} issues")
            return issues
            
        except Exception as e:
            logger.error(f"Error searching issues: {e}")
            return []
    
    async def search_recent_issues(self, days: int = 7, max_results: int = 50) -> List[Dict]:
        """
        Search for recent issues using working pattern
        
        Args:
            days: Number of days to look back
            max_results: Maximum number of results
        
        Returns:
            List of recent issues
        """
        jql = f"created >= -{days}d ORDER BY created DESC"
        return await self.run(jql, max_results)
    
    async def search_project_issues(self, project_key: str, max_results: int = 50) -> List[Dict]:
        """
        Search for issues in a specific project
        
        Args:
            project_key: Project key (e.g., 'KAN')
            max_results: Maximum number of results
        
        Returns:
            List of project issues
        """
        jql = f"project = {project_key} ORDER BY created DESC"
        return await self.run(jql, max_results)
    
    async def search_my_issues(self, max_results: int = 50) -> List[Dict]:
        """
        Search for issues assigned to current user
        
        Args:
            max_results: Maximum number of results
        
        Returns:
            List of assigned issues
        """
        jql = "assignee = currentUser() ORDER BY updated DESC"
        return await self.run(jql, max_results) 