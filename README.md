# JIRA MCP Server

A custom MCP (Model Context Protocol) server for JIRA integration, built using proven working patterns from existing JIRA API integration scripts.

## 🎯 **Overview**

This MCP server provides tools for:
- ✅ Creating JIRA issues
- ✅ Searching JIRA issues using JQL
- ✅ Updating JIRA issues
- ✅ Discovering JIRA projects

## ✅ **Proven Working Configuration**

This server uses the following proven working configuration:
- **Cloud ID:** `7a2d59af-fc96-40e2-8122-8d0b7b8fb180`
- **Site:** `https://pushpiinder.atlassian.net`
- **Project:** `KAN` (LedgerClient)
- **API Patterns:** Extracted from working integration scripts

## 🏗️ **Architecture**

```
src/
├── server.py              # Main MCP server entry point
├── tools/
│   ├── issue_tools.py     # Issue creation and updates
│   ├── search_tools.py    # Issue search functionality
│   └── project_tools.py   # Project discovery
├── clients/
│   └── jira_client.py     # JIRA API client
└── config/
    └── settings.py        # Configuration management
```

## 🚀 **Quick Start**

### 1. **Clone and Setup**

```bash
git clone <repository-url>
cd jira-mcp-server
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Configure Environment**

Copy the environment template and configure your JIRA credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values:
```bash
# Required - Get from Atlassian
JIRA_API_TOKEN=your_api_token_here
JIRA_USER_EMAIL=your_email@example.com

# Working configuration (already set)
JIRA_CLOUD_ID=7a2d59af-fc96-40e2-8122-8d0b7b8fb180
JIRA_BASE_URL=https://pushpiinder.atlassian.net
JIRA_PROJECT_KEY=KAN
```

### 4. **Run the Server**

```bash
python src/server.py
```

## 🛠️ **Available Tools**

### **Create Issue**
```python
# Create a new JIRA issue
await create_jira_issue(
    project_key="KAN",
    summary="Test issue",
    description="This is a test issue",
    issue_type="Task"
)
```

### **Search Issues**
```python
# Search issues using JQL
await search_jira_issues(
    jql="created >= -7d ORDER BY created DESC",
    max_results=50
)
```

### **Get Projects**
```python
# Get visible projects
await get_jira_projects()
```

### **Update Issue**
```python
# Update an existing issue
await update_jira_issue(
    issue_key="KAN-123",
    fields={"summary": "Updated summary"}
)
```

## 🐳 **Docker Deployment**

### **Build Image**
```bash
docker build -t jira-mcp-server .
```

### **Run Container**
```bash
docker run -p 8080:8080 --env-file .env jira-mcp-server
```

## ☁️ **Cloud Run Deployment**

### **1. Build and Push to Google Container Registry**

```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id

# Build and tag
docker build -t gcr.io/$PROJECT_ID/jira-mcp-server .

# Push to registry
docker push gcr.io/$PROJECT_ID/jira-mcp-server
```

### **2. Deploy to Cloud Run**

```bash
gcloud run deploy jira-mcp-server \
  --image gcr.io/$PROJECT_ID/jira-mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars JIRA_CLOUD_ID=7a2d59af-fc96-40e2-8122-8d0b7b8fb180 \
  --set-env-vars JIRA_BASE_URL=https://pushpiinder.atlassian.net \
  --set-env-vars JIRA_PROJECT_KEY=KAN
```

### **3. Set Secrets (Recommended)**

```bash
# Create secrets
echo -n "your-api-token" | gcloud secrets create jira-api-token --data-file=-
echo -n "your-email" | gcloud secrets create jira-user-email --data-file=-

# Update deployment to use secrets
gcloud run services update jira-mcp-server \
  --set-secrets JIRA_API_TOKEN=jira-api-token:latest \
  --set-secrets JIRA_USER_EMAIL=jira-user-email:latest
```

## 🔧 **Configuration**

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `JIRA_CLOUD_ID` | JIRA Cloud ID | `7a2d59af-fc96-40e2-8122-8d0b7b8fb180` |
| `JIRA_BASE_URL` | JIRA site URL | `https://pushpiinder.atlassian.net` |
| `JIRA_PROJECT_KEY` | Default project key | `KAN` |
| `JIRA_API_TOKEN` | API token (required) | - |
| `JIRA_USER_EMAIL` | User email (required) | - |
| `MAX_RESULTS` | Default max results | `50` |
| `DEFAULT_ISSUE_TYPE` | Default issue type | `Task` |

## 📝 **Working Patterns**

This server uses proven working patterns from existing integration scripts:

### **✅ Correct Parameter Names**
- `issueTypeName` (not `issueType`)
- `projectKey` (not `projectIdOrKey`)
- `maxResults` (not `max_results`)

### **✅ Response Parsing**
```python
# Standard response parsing pattern
if response and "result" in response and "content" in response["result"]:
    content = response["result"]["content"]
    if content and len(content) > 0:
        result_data = json.loads(content[0]["text"])
```

### **✅ Error Handling**
```python
# Standard error handling
if "key" in result_data:
    print(f"✅ Success: {result_data['key']}")
elif "error" in result_data:
    print(f"❌ Error: {result_data['error']}")
```

## 🧪 **Testing**

### **Run Tests**
```bash
pytest tests/
```

### **Test Individual Tools**
```bash
# Test issue creation
python -c "
import asyncio
from src.tools.issue_tools import CreateIssueTool
from src.clients.jira_client import JiraClient

async def test():
    client = JiraClient('https://pushpiinder.atlassian.net', 'token', 'cloud-id')
    tool = CreateIssueTool(client)
    result = await tool.run('KAN', 'Test', 'Description')
    print(result)

asyncio.run(test())
"
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Authentication Error**
   - Verify `JIRA_API_TOKEN` is correct
   - Ensure `JIRA_USER_EMAIL` matches token owner

2. **Project Not Found**
   - Verify `JIRA_PROJECT_KEY` exists
   - Check user has access to project

3. **Connection Issues**
   - Verify `JIRA_BASE_URL` is correct
   - Check network connectivity

### **Logs**

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python src/server.py
```

## 📚 **API Reference**

### **JiraClient Methods**

- `create_issue(project_key, summary, description, issue_type)`
- `search_issues(jql, max_results)`
- `get_projects()`
- `update_issue(issue_key, fields)`

### **Tool Classes**

- `CreateIssueTool` - Create new issues
- `UpdateIssueTool` - Update existing issues
- `SearchIssuesTool` - Search issues with JQL
- `GetProjectsTool` - Discover projects

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

MIT License - see LICENSE file for details.

---

**Built with proven working patterns from existing JIRA integration scripts** 🚀 