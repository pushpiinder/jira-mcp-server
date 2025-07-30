#!/usr/bin/env python3
"""
Test script to verify configuration loading
"""

import sys
import os
sys.path.append('src')

from config.settings import Settings

def test_config():
    """Test that configuration loads correctly"""
    try:
        settings = Settings()
        
        print("✅ Configuration loaded successfully!")
        print(f"JIRA URL: {settings.jira_base_url}")
        print(f"JIRA Username: {settings.jira_user_email}")
        print(f"JIRA Cloud ID: {settings.jira_cloud_id}")
        print(f"JIRA Project Key: {settings.jira_project_key}")
        print(f"SSL Verify: {settings.jira_ssl_verify}")
        
        # Check if token is loaded (don't print the actual token)
        if settings.jira_api_token:
            print(f"JIRA Token: {'*' * 20} (loaded)")
        else:
            print("❌ JIRA Token: Not loaded")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    test_config() 