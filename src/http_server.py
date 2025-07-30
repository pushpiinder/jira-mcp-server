"""
HTTP Server wrapper for JIRA MCP Server
This allows the MCP server to run on Cloud Run as an HTTP service
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from config.settings import Settings
from clients.jira_client import JiraClient
from tools.jira_tools import create_jira_issue, update_jira_issue, search_jira_issues, get_jira_projects

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="JIRA MCP Server", version="1.0.0")

# Global client instance
jira_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize JIRA client when server starts"""
    global jira_client
    
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

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when server shuts down"""
    global jira_client
    if jira_client:
        await jira_client.close()
        logger.info("✅ JIRA client closed")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "JIRA MCP Server"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "JIRA MCP Server"}

@app.post("/tools/call")
async def call_tool(request: Dict[str, Any]):
    """Handle MCP tool calls via HTTP"""
    global jira_client
    
    if not jira_client:
        raise HTTPException(status_code=500, detail="JIRA client not initialized")
    
    try:
        tool_name = request.get("name")
        arguments = request.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")
        
        # Route to appropriate tool
        if tool_name == "create_jira_issue":
            result = await create_jira_issue(
                project_key=arguments.get("project_key"),
                summary=arguments.get("summary"),
                description=arguments.get("description"),
                issue_type=arguments.get("issue_type", "Task")
            )
        elif tool_name == "update_jira_issue":
            result = await update_jira_issue(
                issue_key=arguments.get("issue_key"),
                fields=arguments.get("fields", {})
            )
        elif tool_name == "search_jira_issues":
            result = await search_jira_issues(
                jql=arguments.get("jql"),
                max_results=arguments.get("max_results", 50)
            )
        elif tool_name == "get_jira_projects":
            result = await get_jira_projects()
        elif tool_name == "search_recent_issues":
            result = await search_jira_issues(
                jql=f"updated >= -{arguments.get('days', 7)}d",
                max_results=arguments.get("max_results", 50)
            )
        elif tool_name == "search_project_issues":
            result = await search_jira_issues(
                jql=f"project = {arguments.get('project_key')}",
                max_results=arguments.get("max_results", 50)
            )
        elif tool_name == "search_my_issues":
            result = await search_jira_issues(
                jql="assignee = currentUser()",
                max_results=arguments.get("max_results", 50)
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        return {"result": result}
        
    except Exception as e:
        logger.error(f"Error calling tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def list_tools():
    """List available tools"""
    return {
        "tools": [
            {
                "name": "create_jira_issue",
                "description": "Create a new JIRA issue",
                "parameters": {
                    "project_key": "string",
                    "summary": "string", 
                    "description": "string",
                    "issue_type": "string (optional, default: Task)"
                }
            },
            {
                "name": "update_jira_issue",
                "description": "Update an existing JIRA issue",
                "parameters": {
                    "issue_key": "string",
                    "fields": "object"
                }
            },
            {
                "name": "search_jira_issues",
                "description": "Search JIRA issues using JQL",
                "parameters": {
                    "jql": "string",
                    "max_results": "number (optional, default: 50)"
                }
            },
            {
                "name": "get_jira_projects",
                "description": "Get list of JIRA projects",
                "parameters": {}
            },
            {
                "name": "search_recent_issues",
                "description": "Search recently updated issues",
                "parameters": {
                    "days": "number (optional, default: 7)",
                    "max_results": "number (optional, default: 50)"
                }
            },
            {
                "name": "search_project_issues",
                "description": "Search issues in a specific project",
                "parameters": {
                    "project_key": "string",
                    "max_results": "number (optional, default: 50)"
                }
            },
            {
                "name": "search_my_issues",
                "description": "Search issues assigned to current user",
                "parameters": {
                    "max_results": "number (optional, default: 50)"
                }
            }
        ]
    }

if __name__ == "__main__":
    # Get port from environment (Cloud Run sets PORT)
    port = int(os.environ.get("PORT", 8080))
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=port) 