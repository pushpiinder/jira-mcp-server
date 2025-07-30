"""
JIRA Issue Tools for MCP Server
Using proven working patterns from WORKING_CODE_EXAMPLES.py
"""

import logging
from typing import Optional, Dict, Any
from mcp.server.models import Tool
from clients.jira_client import JiraClient

logger = logging.getLogger(__name__)

class CreateIssueTool(Tool):
    """Create JIRA issue using working pattern"""
    
    def __init__(self, jira_client: JiraClient):
        self.jira_client = jira_client
        super().__init__()
    
    name = "create_jira_issue"
    description = "Create a new JIRA issue using proven working patterns"
    
    async def run(
        self, 
        project_key: str, 
        summary: str, 
        description: str, 
        issue_type: str = "Task"
    ) -> Optional[str]:
        """
        Create a JIRA issue using the working pattern from examples
        
        Args:
            project_key: Project key (e.g., 'KAN')
            summary: Issue summary
            description: Issue description
            issue_type: Issue type (default: 'Task')
        
        Returns:
            Issue key if successful, None otherwise
        """
        try:
            logger.info(f"Creating issue in project {project_key}: {summary}")
            
            # Use the working pattern from examples
            issue_key = await self.jira_client.create_issue(
                project_key=project_key,
                summary=summary,
                description=description,
                issue_type=issue_type
            )
            
            if issue_key:
                logger.info(f"✅ Successfully created issue: {issue_key}")
                return issue_key
            else:
                logger.error("❌ Failed to create issue")
                return None
                
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return None

class UpdateIssueTool(Tool):
    """Update JIRA issue using working pattern"""
    
    def __init__(self, jira_client: JiraClient):
        self.jira_client = jira_client
        super().__init__()
    
    name = "update_jira_issue"
    description = "Update an existing JIRA issue using proven working patterns"
    
    async def run(
        self, 
        issue_key: str, 
        fields: Dict[str, Any]
    ) -> bool:
        """
        Update a JIRA issue using the working pattern
        
        Args:
            issue_key: Issue key to update (e.g., 'KAN-123')
            fields: Fields to update (e.g., {'summary': 'New summary'})
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Updating issue {issue_key}")
            
            # Use the working pattern from examples
            success = await self.jira_client.update_issue(
                issue_key=issue_key,
                fields=fields
            )
            
            if success:
                logger.info(f"✅ Successfully updated issue: {issue_key}")
            else:
                logger.error(f"❌ Failed to update issue: {issue_key}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating issue: {e}")
            return False 