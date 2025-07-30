"""
JIRA Tools using FastMCP
Clean, modern tool implementations with decorators
"""

import logging
from typing import List, Dict, Optional, Any
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Get the FastMCP instance from server
mcp = FastMCP("jira-mcp-server")

@mcp.tool()
async def create_jira_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> Optional[str]:
    """
    Create a new JIRA issue using direct REST API.
    
    **Input:**
    - project_key: Project key (e.g., 'KAN')
    - summary: Issue summary
    - description: Issue description
    - issue_type: Issue type (default: 'Task')
    
    **Output:** Issue key if successful, None otherwise
    
    **Example:** "Create a bug ticket for the login issue"
    """
    try:
        from server import jira_client
        
        if not jira_client:
            logger.error("❌ JIRA client not initialized")
            return None
        
        logger.info(f"Creating issue in project {project_key}: {summary}")
        
        issue_key = await jira_client.create_issue(
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

@mcp.tool()
async def update_jira_issue(issue_key: str, fields: Dict[str, Any]) -> bool:
    """
    Update an existing JIRA issue.
    
    **Input:**
    - issue_key: Issue key to update (e.g., 'KAN-123')
    - fields: Fields to update (e.g., {'summary': 'New summary'})
    
    **Output:** True if successful, False otherwise
    
    **Example:** "Update the summary of KAN-123 to 'Fixed login bug'"
    """
    try:
        from server import jira_client
        
        if not jira_client:
            logger.error("❌ JIRA client not initialized")
            return False
        
        logger.info(f"Updating issue {issue_key}")
        
        success = await jira_client.update_issue(
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

@mcp.tool()
async def search_jira_issues(jql: str, max_results: int = 50) -> List[Dict]:
    """
    Search JIRA issues using JQL with direct REST API.
    
    **Input:**
    - jql: JQL query string (e.g., 'created >= -7d ORDER BY created DESC')
    - max_results: Maximum number of results to return
    
    **Output:** List of issues matching the query
    
    **Example:** "Find all open bugs in the KAN project"
    """
    try:
        from server import jira_client
        
        if not jira_client:
            logger.error("❌ JIRA client not initialized")
            return []
        
        logger.info(f"Searching issues with JQL: {jql}")
        
        issues = await jira_client.search_issues(
            jql=jql,
            max_results=max_results
        )
        
        logger.info(f"✅ Found {len(issues)} issues")
        return issues
        
    except Exception as e:
        logger.error(f"Error searching issues: {e}")
        return []

@mcp.tool()
async def get_jira_projects() -> List[Dict]:
    """
    Get visible JIRA projects using direct REST API.
    
    **Input:** None
    
    **Output:** List of visible projects
    
    **Example:** "Show me all available JIRA projects"
    """
    try:
        from server import jira_client
        
        if not jira_client:
            logger.error("❌ JIRA client not initialized")
            return []
        
        logger.info("Getting visible JIRA projects")
        
        projects = await jira_client.get_projects()
        
        logger.info(f"✅ Found {len(projects)} projects")
        return projects
        
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        return []

@mcp.tool()
async def search_recent_issues(days: int = 7, max_results: int = 50) -> List[Dict]:
    """
    Search for recent issues created in the last N days.
    
    **Input:**
    - days: Number of days to look back (default: 7)
    - max_results: Maximum number of results (default: 50)
    
    **Output:** List of recent issues
    
    **Example:** "Show me issues created in the last 3 days"
    """
    jql = f"created >= -{days}d ORDER BY created DESC"
    return await search_jira_issues(jql, max_results)

@mcp.tool()
async def search_project_issues(project_key: str, max_results: int = 50) -> List[Dict]:
    """
    Search for issues in a specific project.
    
    **Input:**
    - project_key: Project key (e.g., 'KAN')
    - max_results: Maximum number of results (default: 50)
    
    **Output:** List of project issues
    
    **Example:** "Show me all issues in the KAN project"
    """
    jql = f"project = {project_key} ORDER BY created DESC"
    return await search_jira_issues(jql, max_results)

@mcp.tool()
async def search_my_issues(max_results: int = 50) -> List[Dict]:
    """
    Search for issues assigned to the current user.
    
    **Input:**
    - max_results: Maximum number of results (default: 50)
    
    **Output:** List of assigned issues
    
    **Example:** "Show me all issues assigned to me"
    """
    jql = "assignee = currentUser() ORDER BY updated DESC"
    return await search_jira_issues(jql, max_results) 