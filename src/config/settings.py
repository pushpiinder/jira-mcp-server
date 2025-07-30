"""
Configuration settings for JIRA MCP Server
Using proven working configuration from WORKING_CODE_EXAMPLES.py
"""

import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from pydantic import Field

class Settings(BaseSettings):
    """JIRA MCP Server configuration settings"""
    
    # ✅ WORKING CONFIGURATION - Proven to work
    jira_cloud_id: str = "7a2d59af-fc96-40e2-8122-8d0b7b8fb180"
    jira_base_url: str = Field(default="https://pushpiinder.atlassian.net", alias="JIRA_URL")
    jira_project_key: str = "KAN"
    jira_project_name: str = "LedgerClient"
    
    # Authentication (from your .env)
    jira_api_token: Optional[str] = Field(default=None, alias="JIRA_TOKEN")
    jira_user_email: Optional[str] = Field(default=None, alias="JIRA_USERNAME")
    jira_ssl_verify: bool = Field(default=True, alias="JIRA_SSL_VERIFY")
    
    # Server configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8080
    
    # API configuration
    max_results: int = 50
    default_issue_type: str = "Task"
    
    # Additional environment variables
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from environment
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Validate required settings
        if not self.jira_api_token:
            raise ValueError("JIRA_API_TOKEN is required")
        if not self.jira_user_email:
            raise ValueError("JIRA_USER_EMAIL is required")
    
    @property
    def working_config(self) -> dict:
        """Return the proven working configuration"""
        return {
            "cloud_id": self.jira_cloud_id,
            "site_url": self.jira_base_url,
            "project_key": self.jira_project_key,
            "project_name": self.jira_project_name
        }
    
    @property
    def working_params(self) -> dict:
        """Return the proven working parameter patterns"""
        return {
            "issue_creation": {
                "cloudId": self.jira_cloud_id,
                "projectKey": self.jira_project_key,
                "issueTypeName": self.default_issue_type
            },
            "issue_search": {
                "cloudId": self.jira_cloud_id,
                "maxResults": self.max_results
            },
            "project_discovery": {
                "cloudId": self.jira_cloud_id
            }
        } 