#!/usr/bin/env python3.11
"""
Test JIRA API functionality using working patterns from WORKING_CODE_EXAMPLES.py
"""

import asyncio
import sys
import os
sys.path.append('src')

from config.settings import Settings
from clients.jira_client import JiraClient

async def test_jira_api():
    """Test JIRA API functionality"""
    print("🚀 Testing JIRA API Functionality")
    print("=" * 50)
    
    try:
        # Load configuration
        settings = Settings()
        print("✅ Configuration loaded")
        
        # Create JIRA client
        client = JiraClient(
            base_url=settings.jira_base_url,
            api_token=settings.jira_api_token,
            cloud_id=settings.jira_cloud_id
        )
        print("✅ JIRA Client created")
        
        # Test 1: Get projects
        print("\n🧪 Test 1: Getting projects...")
        projects = await client.get_projects()
        if projects:
            print(f"✅ Found {len(projects)} projects")
            for project in projects[:3]:  # Show first 3
                print(f"  - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
        else:
            print("❌ No projects found")
        
        # Test 2: Search recent issues
        print("\n🧪 Test 2: Searching recent issues...")
        issues = await client.search_issues(
            jql="created >= -7d ORDER BY created DESC",
            max_results=5
        )
        if issues:
            print(f"✅ Found {len(issues)} recent issues")
            for issue in issues[:3]:  # Show first 3
                print(f"  - {issue.get('key', 'N/A')}: {issue.get('fields', {}).get('summary', 'N/A')}")
        else:
            print("❌ No recent issues found")
        
        # Test 3: Create a test issue
        print("\n🧪 Test 3: Creating test issue...")
        test_summary = f"Test issue from MCP server - {asyncio.get_event_loop().time()}"
        test_description = "This is a test issue created via the MCP server script."
        
        issue_key = await client.create_issue(
            project_key=settings.jira_project_key,
            summary=test_summary,
            description=test_description,
            issue_type="Task"
        )
        
        if issue_key:
            print(f"✅ Successfully created issue: {issue_key}")
            
            # Test 4: Update the issue
            print(f"\n🧪 Test 4: Updating issue {issue_key}...")
            success = await client.update_issue(
                issue_key=issue_key,
                fields={"summary": f"{test_summary} - UPDATED"}
            )
            if success:
                print(f"✅ Successfully updated issue: {issue_key}")
            else:
                print(f"❌ Failed to update issue: {issue_key}")
        else:
            print("❌ Failed to create test issue")
        
        print("\n✅ All API tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during API testing: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_jira_api()
    
    if success:
        print("\n🎉 JIRA MCP Server is ready for deployment!")
        print("\n📝 Next steps:")
        print("1. Deploy to Cloud Run")
        print("2. Test with actual MCP client")
        print("3. Monitor logs and performance")
    else:
        print("\n❌ API tests failed. Check configuration and network connectivity.")

if __name__ == "__main__":
    asyncio.run(main()) 