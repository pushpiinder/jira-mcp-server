#!/usr/bin/env python3
"""
JIRA MCP Server
Main server entry point using proven working patterns from WORKING_CODE_EXAMPLES.py
"""

import asyncio
import json
import logging
from typing import Dict, Optional, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

# Import custom tools
from tools.issue_tools import CreateIssueTool, UpdateIssueTool
from tools.search_tools import SearchIssuesTool
from tools.project_tools import GetProjectsTool

# Import JIRA client
from clients.jira_client import JiraClient

# Import configuration
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JiraMCPServer:
    """Main JIRA MCP Server using proven working patterns"""
    
    def __init__(self):
        self.settings = Settings()
        self.jira_client = JiraClient(
            base_url=self.settings.jira_base_url,
            api_token=self.settings.jira_api_token,
            cloud_id=self.settings.jira_cloud_id,
            username=self.settings.jira_user_email
        )
        
        # Initialize MCP server
        self.server = Server("jira-mcp-server")
        
        # Register tools using working patterns
        self.server.list_tools(
            CreateIssueTool(self.jira_client),
            UpdateIssueTool(self.jira_client),
            SearchIssuesTool(self.jira_client),
            GetProjectsTool(self.jira_client)
        )
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting JIRA MCP Server...")
        logger.info(f"Using Cloud ID: {self.settings.jira_cloud_id}")
        logger.info(f"Using Site: {self.settings.jira_base_url}")
        logger.info(f"Using Project: {self.settings.jira_project_key}")
        
        try:
            await stdio_server(self.server)
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise

async def main():
    """Main entry point"""
    server = JiraMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main()) 