# Day 8: MCP (Model Context Protocol) Continued - Building & Implementation

**Date:** September 27, 2026  
**Topic:** MCP Part 2 - Building Custom MCP Servers  
**Level:** Intermediate to Advanced

---

## Overview

After understanding MCP architecture (Day 7), Day 8 focuses on **practical implementation**: building actual MCP servers, integrating them with Claude, and deploying them for real-world applications.

---

## Lesson 1: Introduction to MCP Development & Practical Tools

### Important Points:

**1. Why Build Custom MCP Servers?**
```
Instead of: API → Claude → Parser → Result
With MCP: Direct tool integration → Cleaner architecture
```

- Standardized interface for any tool/data source
- Seamless integration with Claude and other AI models
- Reduces boilerplate code significantly
- Future-proof: works with any MCP-compatible AI model

**2. Development Environment Setup**

Essential Tools:
```
├─ Python 3.8+ (recommended: 3.10+)
│  └─ Primary language for MCP servers
│
├─ Claude Desktop / VS Code
│  └─ IDE for development
│
├─ GitHub
│  └─ Version control & sharing MCP servers
│
├─ Optional IDEs:
│  ├─ Visual Studio Code (most popular)
│  ├─ PyCharm
│  └─ Cursor IDE (AI-assisted development)
│
└─ Testing Tools:
   └─ Jupyter Notebooks (interactive testing)
```

**3. MCP Framework Options**

Official MCP SDK:
```python
# Python SDK from Anthropic
pip install mcp

# Core components:
├─ Server class (base for your MCP)
├─ Tools decorator (@tool)
├─ Request/Response handlers
└─ Transport layer (stdio, HTTP, WebSocket)
```

**4. IDE Choice & Setup**

**Visual Studio Code (Recommended):**
- Extensions: Python, MCP, REST Client
- Git integration built-in
- Lightweight, widely used
- Good MCP documentation support

**Cursor IDE (Advanced):**
- AI-assisted code generation
- Better for rapid MCP development
- Understands MCP patterns
- Faster implementation

**PyCharm (Professional):**
- Full-featured IDE
- Excellent debugging
- Built-in testing framework
- Heavier resource usage

**5. MCP Server Architecture**

```
┌─────────────────────────────┐
│  Your MCP Server (Python)   │
├─────────────────────────────┤
│  1. Tool Definitions        │
│     - tool1(), tool2(), ... │
├─────────────────────────────┤
│  2. Handler Functions       │
│     - Process requests      │
│     - Return results        │
├─────────────────────────────┤
│  3. Transport Layer         │
│     - stdio / HTTP / WS     │
└─────────────────────────────┘
         ↓↑
┌─────────────────────────────┐
│  Claude / AI Application    │
└─────────────────────────────┘
```

### Practical Implementation:

**Step 1: Create Basic MCP Server**

```python
# mcp_server.py
from mcp import Server, Tool
import json

# Initialize server
server = Server(name="MyFirstMCP")

# Define a simple tool
@server.tool()
def greet(name: str) -> str:
    """Greet a person by name"""
    return f"Hello, {name}! Welcome to MCP."

# Define another tool
@server.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Register tools
server.register_tool(greet)
server.register_tool(add_numbers)

if __name__ == "__main__":
    server.run()
```

**Step 2: Tool Definition (JSON Schema)**

Each tool needs specification:
```json
{
  "name": "greet",
  "description": "Greet a person by name",
  "input_schema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Person's name"
      }
    },
    "required": ["name"]
  }
}
```

**Step 3: Testing Locally**

```python
# test_mcp.py
from mcp_server import server

# Test without Claude
result = server.tools['greet']("Alice")
print(result)  # "Hello, Alice! Welcome to MCP."

result = server.tools['add_numbers'](5, 3)
print(result)  # 8
```

---

## Lesson 2: Demo - Real MCP Implementation with Claude Desktop

### Important Points:

**1. Configuration File (mcp_config.json)**

MCP servers are registered through config:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["-m", "mcp.server.filesystem"],
      "disabled": false
    },
    "my-custom-server": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "disabled": false,
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

**2. Claude Desktop Integration**

Configuration location:
```
Mac: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
```

After configuring, Claude Desktop immediately sees your tools:
- No restart needed
- Tools available in chat interface
- Claude can call them automatically

**3. Tool Availability in Claude**

Once configured:
```
User: "Can you greet Alice and add 5 + 3?"

Claude: "I'll use the MCP tools to do that."
         [Calls: greet("Alice"), add_numbers(5, 3)]
         
Result: "Hello, Alice! Welcome to MCP. And 5 + 3 = 8."
```

**4. Environment Variables & Secrets**

Safe credential handling:
```json
{
  "my-database-server": {
    "command": "python",
    "args": ["/path/to/db_mcp.py"],
    "env": {
      "DB_HOST": "localhost",
      "DB_USER": "admin",
      "DB_PASSWORD": "${DB_PASSWORD}"  // From system env
    }
  }
}
```

**5. Logging & Debugging**

Enable debugging:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MyMCP")

@server.tool()
def my_function():
    logger.debug("Function called")
    # implementation
    logger.info("Function completed")
```

Check logs:
```
Mac/Linux: tail -f ~/.mcp/debug.log
Windows: Get-Content "Logs\mcp.log" -Wait
```

### Practical Implementation:

**Example 1: Database Query MCP**

```python
# db_mcp_server.py
from mcp import Server, Tool
import sqlite3

server = Server(name="DatabaseMCP")

@server.tool()
def query_users(department: str) -> list:
    """Get all users in a department"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE department = ?", (department,))
    results = cursor.fetchall()
    conn.close()
    return results

@server.tool()
def add_user(name: str, email: str, department: str) -> bool:
    """Add a new user to database"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, department) VALUES (?, ?, ?)",
        (name, email, department)
    )
    conn.commit()
    conn.close()
    return True

@server.tool()
def get_department_stats(department: str) -> dict:
    """Get statistics for a department"""
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as count,
            AVG(salary) as avg_salary,
            MIN(start_date) as earliest
        FROM users 
        WHERE department = ?
    """, (department,))
    result = cursor.fetchone()
    conn.close()
    return {
        "employee_count": result[0],
        "avg_salary": result[1],
        "earliest_hire": result[2]
    }

server.register_tools([query_users, add_user, get_department_stats])
```

**Example 2: File Operations MCP**

```python
# file_mcp_server.py
from mcp import Server, Tool
import os
import json

server = Server(name="FileOperationsMCP")

@server.tool()
def read_file(file_path: str) -> str:
    """Read contents of a file"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"

@server.tool()
def write_file(file_path: str, content: str) -> bool:
    """Write content to a file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

@server.tool()
def list_directory(dir_path: str) -> list:
    """List files in a directory"""
    try:
        return os.listdir(dir_path)
    except FileNotFoundError:
        return []

@server.tool()
def search_files(directory: str, pattern: str) -> list:
    """Search for files matching pattern"""
    import fnmatch
    matches = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                matches.append(os.path.join(root, file))
    return matches

server.register_tools([read_file, write_file, list_directory, search_files])
```

---

## Lesson 3: Building Custom MCP Servers - Step-by-Step

### Important Points:

**1. Server Architecture Decision**

What type of server to build?
```
Data Access MCP
├─ Connect to databases
├─ Query data
└─ Update/delete records
└─ Example: DatabaseMCP, APIMcp

File Operations MCP
├─ Read/write files
├─ Directory operations
└─ Search filesystem
└─ Example: FileSystemMCP, CodeEditorMCP

Integration MCP
├─ Connect to external APIs
├─ Fetch real-time data
├─ Execute workflows
└─ Example: SlackMCP, GitHubMCP, AzureMCP

Analysis MCP
├─ Process data
├─ Run calculations
├─ Generate reports
└─ Example: DataAnalysisMCP, ReportMCP
```

**2. Security Considerations**

Critical in production:
```python
# ✓ DO: Use environment variables for secrets
import os
api_key = os.getenv('API_KEY')
db_password = os.getenv('DB_PASSWORD')

# ✗ DON'T: Hardcode credentials
api_key = "sk-1234567890"  # NEVER DO THIS

# ✓ DO: Validate inputs
def delete_record(record_id: int) -> bool:
    if record_id < 0:
        raise ValueError("Invalid record ID")
    # safe to proceed

# ✗ DON'T: Accept raw user input
def delete_record(record_id: str) -> bool:
    query = f"DELETE FROM users WHERE id = {record_id}"  # SQL INJECTION!
    
# ✓ DO: Use parameterized queries
cursor.execute("DELETE FROM users WHERE id = ?", (record_id,))

# ✓ DO: Rate limit to prevent abuse
from functools import wraps
import time

def rate_limit(calls=100, period=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check rate limit
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**3. Error Handling**

Robust MCP servers handle errors gracefully:
```python
@server.tool()
def risky_operation(input_data: str) -> dict:
    """Perform risky operation with error handling"""
    try:
        # Attempt operation
        result = process_data(input_data)
        return {
            "success": True,
            "data": result
        }
    except ValueError as e:
        # Handle validation errors
        return {
            "success": False,
            "error": f"Validation error: {str(e)}"
        }
    except TimeoutError as e:
        # Handle timeout
        return {
            "success": False,
            "error": "Operation timed out"
        }
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error: {e}")
        return {
            "success": False,
            "error": "Internal server error"
        }
```

**4. Testing MCP Servers**

Comprehensive testing:
```python
# test_custom_mcp.py
import pytest
from mcp_server import server

class TestCustomMCP:
    
    def test_valid_input(self):
        result = server.tools['my_function']("valid_input")
        assert result is not None
    
    def test_invalid_input(self):
        with pytest.raises(ValueError):
            server.tools['my_function']("invalid_input")
    
    def test_error_handling(self):
        result = server.tools['risky_operation']("bad_data")
        assert result['success'] == False
    
    def test_performance(self):
        import time
        start = time.time()
        server.tools['fast_operation']()
        duration = time.time() - start
        assert duration < 1.0  # Should complete in 1 second

# Run tests
# pytest test_custom_mcp.py
```

**5. Deployment Options**

Where to run your MCP server:
```
Local (Development)
├─ Run on your machine
├─ Test with Claude Desktop
└─ Easy debugging

Cloud Deployment (Production)
├─ AWS EC2 / Lambda
├─ Google Cloud Run
├─ Azure Functions
├─ Heroku
└─ Benefits: 24/7 availability, scalability

Docker Container
├─ Reproducible environment
├─ Easy scaling
├─ Platform-agnostic
└─ Good for production

Example Docker setup:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "mcp_server.py"]
```
```

### Practical Implementation:

**Complete Example: GitHub Integration MCP**

```python
# github_mcp_server.py
from mcp import Server, Tool
import os
from github import Github
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GitHubMCP")

server = Server(name="GitHubMCP")

# Initialize GitHub client
github_token = os.getenv('GITHUB_TOKEN')
g = Github(github_token)

@server.tool()
def list_repositories(username: str) -> list:
    """List all repositories for a user"""
    try:
        user = g.get_user(username)
        repos = []
        for repo in user.get_repos():
            repos.append({
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "language": repo.language,
                "url": repo.html_url
            })
        return repos
    except Exception as e:
        logger.error(f"Error listing repos: {e}")
        return []

@server.tool()
def get_repository_stats(repo_owner: str, repo_name: str) -> dict:
    """Get detailed stats for a repository"""
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        return {
            "name": repo.name,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "open_issues": repo.open_issues_count,
            "watchers": repo.watchers_count,
            "language": repo.language,
            "created_at": str(repo.created_at),
            "last_update": str(repo.updated_at),
            "contributors": repo.get_contributors().totalCount
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {}

@server.tool()
def search_repositories(query: str, language: str = None) -> list:
    """Search repositories by query and optional language"""
    try:
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        results = []
        for repo in g.search_repositories(search_query, sort="stars"):
            results.append({
                "name": repo.name,
                "owner": repo.owner.login,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "language": repo.language,
                "url": repo.html_url
            })
            if len(results) >= 10:  # Limit to 10 results
                break
        return results
    except Exception as e:
        logger.error(f"Error searching repos: {e}")
        return []

@server.tool()
def get_repo_issues(repo_owner: str, repo_name: str, state: str = "open") -> list:
    """Get issues from a repository"""
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        issues = []
        for issue in repo.get_issues(state=state):
            issues.append({
                "number": issue.number,
                "title": issue.title,
                "state": issue.state,
                "created_at": str(issue.created_at),
                "url": issue.html_url,
                "labels": [label.name for label in issue.labels]
            })
            if len(issues) >= 20:  # Limit to 20 issues
                break
        return issues
    except Exception as e:
        logger.error(f"Error getting issues: {e}")
        return []

# Register all tools
server.register_tools([
    list_repositories,
    get_repository_stats,
    search_repositories,
    get_repo_issues
])

if __name__ == "__main__":
    server.run()
```

**Configuration for Claude Desktop:**

```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["/path/to/github_mcp_server.py"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Usage in Claude:**

```
User: "Find the top 5 most starred Python repositories from OpenAI"

Claude: I'll search for Python repositories from OpenAI.
        [Calls: search_repositories("OpenAI", "Python")]
        
Result: Lists top repositories with star counts and links

User: "Get detailed stats on the top repository"

Claude: [Calls: get_repository_stats("openai", "repo-name")]

Result: Shows stars, forks, contributors, last update, etc.
```

---

## Lesson 4: Advanced MCP Patterns & Best Practices

### Important Points:

**1. Stateful vs Stateless Servers**

```python
# Stateless (Recommended for scalability)
@server.tool()
def calculate(a: int, b: int) -> int:
    return a + b
# No internal state maintained
# Can run multiple instances
# Easy to scale

# Stateful (Use carefully)
class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_id: str) -> str:
        session_id = generate_id()
        self.sessions[session_id] = {"user": user_id, "data": []}
        return session_id
    
    def add_data(self, session_id: str, data: str) -> bool:
        if session_id in self.sessions:
            self.sessions[session_id]["data"].append(data)
            return True
        return False

# Challenges:
# - Memory usage
# - Difficult to scale across instances
# - State persistence needed
```

**2. Caching for Performance**

```python
# Simple caching
from functools import lru_cache

@lru_cache(maxsize=128)
@server.tool()
def expensive_computation(input_val: str) -> str:
    # This result is cached
    return process_data(input_val)

# TTL (Time-To-Live) caching
import time
from functools import wraps

cache = {}
cache_ttl = 300  # 5 minutes

def cached_tool(ttl=cache_ttl):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str((func.__name__, args, tuple(kwargs.items())))
            now = time.time()
            
            if key in cache and (now - cache[key]['time']) < ttl:
                return cache[key]['value']
            
            result = func(*args, **kwargs)
            cache[key] = {'value': result, 'time': now}
            return result
        return wrapper
    return decorator

@cached_tool(ttl=600)
@server.tool()
def fetch_user_data(user_id: int) -> dict:
    # Results cached for 10 minutes
    return database.get_user(user_id)
```

**3. Async Operations**

```python
import asyncio

@server.tool()
async def long_running_operation(duration: int) -> str:
    """Simulate long-running operation"""
    await asyncio.sleep(duration)
    return f"Completed after {duration} seconds"

# Benefits:
# - Non-blocking
# - Handle multiple requests concurrently
# - Better resource utilization
```

**4. Tool Composition**

```python
# Combining tools for complex workflows

@server.tool()
def get_user_orders(user_id: int) -> list:
    """Get all orders for a user"""
    return database.get_orders(user_id)

@server.tool()
def get_order_details(order_id: int) -> dict:
    """Get details for specific order"""
    return database.get_order(order_id)

@server.tool()
def get_user_order_summary(user_id: int) -> dict:
    """Composite: Get all orders and summarize"""
    orders = get_user_orders(user_id)
    total_amount = sum(order['amount'] for order in orders)
    return {
        "user_id": user_id,
        "total_orders": len(orders),
        "total_spent": total_amount,
        "orders": orders
    }

# Claude can:
# 1. Call individual tools (get_user_orders, get_order_details)
# 2. Call composite tool (get_user_order_summary)
# 3. Chain calls together
```

---

## Lesson 5: Real-World Use Cases & Deployment

### Important Points:

**1. Enterprise Integration MCP**

```python
# Connect Claude to enterprise systems

class EnterpriseMCP:
    """Integration with company systems"""
    
    def __init__(self):
        self.crm = CRMClient(os.getenv('CRM_TOKEN'))
        self.erp = ERPClient(os.getenv('ERP_TOKEN'))
        self.hris = HRISClient(os.getenv('HRIS_TOKEN'))
    
    @server.tool()
    def get_customer_info(customer_id: str) -> dict:
        """Fetch customer data from CRM"""
        return self.crm.get_customer(customer_id)
    
    @server.tool()
    def check_inventory(product_id: str) -> dict:
        """Check product inventory in ERP"""
        return self.erp.get_inventory(product_id)
    
    @server.tool()
    def get_employee_info(employee_id: str) -> dict:
        """Get employee data from HRIS"""
        return self.hris.get_employee(employee_id)
    
    @server.tool()
    def create_sales_order(customer_id: str, items: list) -> str:
        """Create sales order spanning CRM and ERP"""
        # Validates customer (CRM) + items (ERP)
        # Creates order in both systems
        return order_id

# Use case:
# "Find customer details, check if items are in stock, create order"
# Claude orchestrates: CRM lookup → ERP check → Order creation
```

**2. Development Assistant MCP**

```python
# Help developers with coding tasks

class DevAssistantMCP:
    """Tools for software development"""
    
    @server.tool()
    def analyze_code(file_path: str) -> dict:
        """Analyze code quality, complexity, security issues"""
        with open(file_path) as f:
            code = f.read()
        return analyzer.analyze(code)
    
    @server.tool()
    def generate_tests(file_path: str) -> str:
        """Generate unit tests for Python file"""
        with open(file_path) as f:
            code = f.read()
        return test_generator.generate(code)
    
    @server.tool()
    def check_dependencies(requirements_file: str) -> list:
        """Check for outdated or vulnerable dependencies"""
        return dependency_checker.audit(requirements_file)
    
    @server.tool()
    def format_code(file_path: str) -> str:
        """Auto-format Python code"""
        with open(file_path) as f:
            code = f.read()
        return formatter.format(code)

# Use case:
# "Analyze my code, generate tests, check for vulnerabilities, format it"
# Claude: [Calls multiple tools] → Returns formatted code with test file
```

**3. Data Analysis MCP**

```python
# Enable Claude to perform data analysis

class DataAnalysisMCP:
    """Statistical analysis and reporting"""
    
    @server.tool()
    def load_data(file_path: str) -> dict:
        """Load CSV/Excel data"""
        df = pd.read_csv(file_path)
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing": df.isnull().sum().to_dict()
        }
    
    @server.tool()
    def statistical_summary(file_path: str, column: str) -> dict:
        """Get statistical summary of column"""
        df = pd.read_csv(file_path)
        return {
            "mean": df[column].mean(),
            "median": df[column].median(),
            "std": df[column].std(),
            "min": df[column].min(),
            "max": df[column].max()
        }
    
    @server.tool()
    def correlation_analysis(file_path: str) -> dict:
        """Find correlations between columns"""
        df = pd.read_csv(file_path)
        return df.corr().to_dict()
    
    @server.tool()
    def groupby_summary(file_path: str, group_col: str, agg_col: str) -> dict:
        """Group data and aggregate"""
        df = pd.read_csv(file_path)
        return df.groupby(group_col)[agg_col].agg(['sum', 'mean', 'count']).to_dict()

# Use case:
# "Load my sales data, show summary stats, find correlations, group by region"
# Claude: [Loads data] → [Analyzes] → [Shows insights with numbers]
```

**4. Deployment Architecture**

Production deployment:
```
                    ┌─────────────────────┐
                    │   Claude Desktop    │
                    │  (User Interface)   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  MCP Configuration  │
                    │   (claude_desktop   │
                    │    _config.json)    │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
    ┌───▼────┐         ┌────────▼───────┐      ┌─────▼────┐
    │ Local  │         │   Cloud API    │      │ Database │
    │Server  │         │  (Lambda/      │      │  Server  │
    │(Dev)   │         │   Cloud Run)   │      │          │
    └────────┘         └────────────────┘      └──────────┘

Production setup:
├─ MCP running on cloud (AWS/GCP/Azure)
├─ Auto-scaling enabled
├─ Security: API keys, rate limiting
├─ Monitoring: Logs, metrics, alerts
└─ Backup: Data redundancy
```

**5. Monitoring & Logging**

```python
import logging
from datetime import datetime
import json

# Structured logging for production
class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_tool_call(self, tool_name: str, inputs: dict, success: bool, duration: float):
        """Log each tool call with metrics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "inputs": inputs,
            "success": success,
            "duration_ms": duration * 1000
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_error(self, tool_name: str, error: Exception):
        """Log errors with context"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "severity": "ERROR"
        }
        self.logger.error(json.dumps(log_entry))

# Usage
logger = StructuredLogger("MyMCP")

@server.tool()
def database_query(query: str) -> list:
    start = time.time()
    try:
        result = db.execute(query)
        duration = time.time() - start
        logger.log_tool_call("database_query", {"query": query}, True, duration)
        return result
    except Exception as e:
        logger.log_error("database_query", e)
        raise
```

---

## Resources & Examples

**Example Servers (GitHub):**
- `filesystem-mcp` - File operations
- `database-mcp` - SQL databases
- `api-wrapper-mcp` - External APIs
- `analytics-mcp` - Data analysis

**Official Documentation:**
- https://modelcontextprotocol.io/
- MCP Python SDK: pip install mcp
- Claude Desktop Configuration

**Community Resources:**
- GitHub: MCP examples and servers

