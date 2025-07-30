"""
JIRA Project Tools for MCP Server
Using proven working patterns from WORKING_CODE_EXAMPLES.py
"""

import logging
from typing import List, Dict, Optional
from mcp.server.models import Tool
from clients.jira_client import JiraClient

logger = logging.getLogger(__name__)

class GetProjectsTool(Tool):
    """Get JIRA projects using working pattern"""
    
    def __init__(self, jira_client: JiraClient):
        self.jira_client = jira_client
        super().__init__()
    
    name = "get_jira_projects"
    description = "Get visible JIRA projects using proven working patterns"
    
    async def run(self) -> List[Dict]:
        """
        Get visible JIRA projects using the working pattern from examples
        
        Returns:
            List of visible projects
        """
        try:
            logger.info("Getting visible JIRA projects")
            
            # Use the working pattern from examples
            projects = await self.jira_client.get_projects()
            
            logger.info(f"✅ Found {len(projects)} projects")
            return projects
            
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return []
    
    async def get_project_by_key(self, project_key: str) -> Optional[Dict]:
        """
        Get a specific project by key
        
        Args:
            project_key: Project key (e.g., 'KAN')
        
        Returns:
            Project data if found, None otherwise
        """
        try:
            projects = await self.run()
            
            for project in projects:
                if project.get("key") == project_key:
                    logger.info(f"✅ Found project: {project_key}")
                    return project
            
            logger.warning(f"Project not found: {project_key}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting project {project_key}: {e}")
            return None
    
    async def get_project_names(self) -> List[str]:
        """
        Get list of project names
        
        Returns:
            List of project names
        """
        try:
            projects = await self.run()
            return [project.get("name", "") for project in projects if project.get("name")]
            
        except Exception as e:
            logger.error(f"Error getting project names: {e}")
            return []
    
    async def get_project_keys(self) -> List[str]:
        """
        Get list of project keys
        
        Returns:
            List of project keys
        """
        try:
            projects = await self.run()
            return [project.get("key", "") for project in projects if project.get("key")]
            
        except Exception as e:
            logger.error(f"Error getting project keys: {e}")
            return [] 