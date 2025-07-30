#!/usr/bin/env python3
"""
Simple test script to verify configuration and basic JIRA client functionality
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
            
        return settings
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return None

def test_jira_client(settings):
    """Test basic JIRA client functionality"""
    try:
        from clients.jira_client import JiraClient
        
        print("\n🧪 Testing JIRA Client...")
        
        client = JiraClient(
            base_url=settings.jira_base_url,
            api_token=settings.jira_api_token,
            cloud_id=settings.jira_cloud_id
        )
        
        print("✅ JIRA Client created successfully")
        print(f"Base URL: {client.base_url}")
        print(f"Cloud ID: {client.cloud_id}")
        
        return client
        
    except Exception as e:
        print(f"❌ JIRA Client error: {e}")
        return None

def main():
    """Main test function"""
    print("🚀 Testing JIRA MCP Server Configuration")
    print("=" * 50)
    
    # Test configuration
    settings = test_config()
    if not settings:
        return
    
    # Test JIRA client
    client = test_jira_client(settings)
    if not client:
        return
    
    print("\n✅ All basic tests passed!")
    print("\n📝 Next steps:")
    print("1. Install MCP package (requires Python 3.10+)")
    print("2. Test actual JIRA API calls")
    print("3. Deploy to Cloud Run")

if __name__ == "__main__":
    main() 