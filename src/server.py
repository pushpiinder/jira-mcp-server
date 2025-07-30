#!/usr/bin/env python3
"""
JIRA MCP Server using FastMCP
Main server entry point with clean FastMCP implementation
"""

import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

# Import configuration and client
from config.settings import Settings
from clients.jira_client import JiraClient

# Import tools (will be converted to FastMCP functions)
from tools.jira_tools import create_jira_issue, update_jira_issue, search_jira_issues, get_jira_projects

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("jira-mcp-server")

# Global client instance
jira_client = None

# Initialize JIRA client
try:
    settings = Settings()
    jira_client = JiraClient(
        base_url=settings.jira_base_url,
        api_token=settings.jira_api_token,
        cloud_id=settings.jira_cloud_id,
        username=settings.jira_user_email
    )
    
    logger.info("✅ JIRA MCP Server initialized successfully")
    logger.info(f"Using Cloud ID: {settings.jira_cloud_id}")
    logger.info(f"Using Site: {settings.jira_base_url}")
    logger.info(f"Using Project: {settings.jira_project_key}")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize JIRA client: {e}")
    raise

async def main():
    """Main entry point"""
    try:
        await stdio_server(mcp)
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 