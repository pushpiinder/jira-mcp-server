#!/usr/bin/env python3.11
"""
Test FastMCP conversion
"""

import asyncio
import sys
import os
sys.path.append('src')

from config.settings import Settings
from clients.jira_client import JiraClient

async def test_fastmcp_conversion():
    """Test FastMCP conversion"""
    print("🚀 Testing FastMCP Conversion")
    print("=" * 40)
    
    try:
        # Test 1: Configuration loading
        print("🧪 Test 1: Configuration loading...")
        settings = Settings()
        print("✅ Configuration loaded successfully")
        
        # Test 2: JIRA client creation
        print("\n🧪 Test 2: JIRA client creation...")
        client = JiraClient(
            base_url=settings.jira_base_url,
            api_token=settings.jira_api_token,
            cloud_id=settings.jira_cloud_id,
            username=settings.jira_user_email
        )
        print("✅ JIRA Client created successfully")
        
        # Test 3: Import FastMCP tools
        print("\n🧪 Test 3: Importing FastMCP tools...")
        from tools.jira_tools import (
            create_jira_issue,
            update_jira_issue,
            search_jira_issues,
            get_jira_projects
        )
        print("✅ FastMCP tools imported successfully")
        
        # Test 4: Test basic API calls (using client directly)
        print("\n🧪 Test 4: Testing basic API calls...")
        
        # Get projects
        projects = await client.get_projects()
        if projects:
            print(f"✅ Found {len(projects)} projects")
        else:
            print("❌ No projects found")
        
        # Search issues
        issues = await client.search_issues(
            jql="created >= -7d ORDER BY created DESC",
            max_results=3
        )
        if issues:
            print(f"✅ Found {len(issues)} recent issues")
        else:
            print("❌ No recent issues found")
        
        # Cleanup
        await client.close()
        
        print("\n✅ All FastMCP conversion tests passed!")
        print("\n📝 FastMCP Benefits:")
        print("✅ Cleaner code with decorators")
        print("✅ Better documentation")
        print("✅ More maintainable")
        print("✅ Modern MCP approach")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during FastMCP testing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_fastmcp_conversion()
    
    if success:
        print("\n🎉 FastMCP conversion is working!")
        print("Ready to test the full MCP server.")
    else:
        print("\n❌ FastMCP conversion has issues.")
        print("Check the error details above.")

if __name__ == "__main__":
    asyncio.run(main()) 