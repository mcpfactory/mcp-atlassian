#
# 代码运行所需的 OS 安装包放在 packages.txt 中，Python安装包放在requirements.txt，请注意都仅放置包名，每个包占一行
#
from typing import Optional
from mcp_factory.server import mcp
from typing import Optional, Dict, Any
from atlassian.tools import JiraTools, ConfluenceTools

# Initialize business logic instances
jira_tools = JiraTools()
confluence_tools = ConfluenceTools()

# =============================================================================
# JIRA TOOLS
# =============================================================================

# 工具：获取Jira问题详情
@mcp.tool(
    name="jira_get_issue",
    description="获取指定Jira问题的详细信息",
    tags=["jira", "read"]
)
def jira_get_issue(issue_key: str, fields: Optional[str] = None, expand: Optional[str] = None) -> str:
    """获取Jira问题详情"""
    return jira_tools.get_issue(issue_key, fields, expand)

# 工具：搜索Jira问题
@mcp.tool(
    name="jira_search_issues",
    description="使用JQL搜索Jira问题",
    tags=["jira", "read"]
)
def jira_search_issues(jql: str, fields: Optional[str] = None, start_at: int = 0, max_results: int = 50) -> str:
    """搜索Jira问题"""
    return jira_tools.search_issues(jql, fields, start_at, max_results)

# 工具：创建Jira问题
@mcp.tool(
    name="jira_create_issue",
    description="创建新的Jira问题",
    tags=["jira", "write"]
)
def jira_create_issue(project_key: str, summary: str, issue_type: str, description: Optional[str] = None, assignee: Optional[str] = None) -> str:
    """创建Jira问题"""
    return jira_tools.create_issue(project_key, summary, issue_type, description, assignee)

# 工具：更新Jira问题
@mcp.tool(
    name="jira_update_issue",
    description="更新现有Jira问题",
    tags=["jira", "write"]
)
def jira_update_issue(issue_key: str, fields: Dict[str, Any]) -> str:
    """更新Jira问题"""
    return jira_tools.update_issue(issue_key, fields)

# 工具：删除Jira问题
@mcp.tool(
    name="jira_delete_issue",
    description="删除Jira问题",
    tags=["jira", "write"]
)
def jira_delete_issue(issue_key: str) -> str:
    """删除Jira问题"""
    return jira_tools.delete_issue(issue_key)

# 工具：添加Jira评论
@mcp.tool(
    name="jira_add_comment",
    description="向Jira问题添加评论",
    tags=["jira", "write"]
)
def jira_add_comment(issue_key: str, comment: str) -> str:
    """添加Jira评论"""
    return jira_tools.add_comment(issue_key, comment)

# 工具：获取Jira问题状态转换
@mcp.tool(
    name="jira_get_transitions",
    description="获取Jira问题的可用状态转换",
    tags=["jira", "read"]
)
def jira_get_transitions(issue_key: str) -> str:
    """获取问题状态转换"""
    return jira_tools.get_transitions(issue_key)

# 工具：转换Jira问题状态
@mcp.tool(
    name="jira_transition_issue",
    description="转换Jira问题到新状态",
    tags=["jira", "write"]
)
def jira_transition_issue(issue_key: str, transition_id: str, fields: Optional[Dict[str, Any]] = None, comment: Optional[str] = None) -> str:
    """转换问题状态"""
    return jira_tools.transition_issue(issue_key, transition_id, fields, comment)

# 工具：获取Jira项目列表
@mcp.tool(
    name="jira_get_projects",
    description="获取所有可访问的Jira项目",
    tags=["jira", "read"]
)
def jira_get_projects() -> str:
    """获取项目列表"""
    return jira_tools.get_projects()

# 工具：获取Jira用户资料
@mcp.tool(
    name="jira_get_user_profile",
    description="获取Jira用户的个人资料信息",
    tags=["jira", "read"]
)
def jira_get_user_profile(user_identifier: str) -> str:
    """获取用户资料"""
    return jira_tools.get_user_profile(user_identifier)

# =============================================================================
# CONFLUENCE TOOLS
# =============================================================================

# 工具：搜索Confluence内容
@mcp.tool(
    name="confluence_search",
    description="搜索Confluence内容",
    tags=["confluence", "read"]
)
def confluence_search(query: str, limit: int = 25, start: int = 0) -> str:
    """搜索Confluence内容"""
    return confluence_tools.search(query, limit, start)

# 工具：获取Confluence页面
@mcp.tool(
    name="confluence_get_page",
    description="获取Confluence页面内容",
    tags=["confluence", "read"]
)
def confluence_get_page(page_id: str, title: str, space_key: str) -> str:
    """获取Confluence页面"""
    return confluence_tools.get_page(page_id, title, space_key)

# 工具：创建Confluence页面
@mcp.tool(
    name="confluence_create_page",
    description="创建新的Confluence页面",
    tags=["confluence", "write"]
)
def confluence_create_page(space_key: str, title: str, content: str, parent_id: Optional[str] = None) -> str:
    """创建Confluence页面"""
    return confluence_tools.create_page(space_key, title, content, parent_id)

# 工具：更新Confluence页面
@mcp.tool(
    name="confluence_update_page",
    description="更新现有Confluence页面",
    tags=["confluence", "write"]
)
def confluence_update_page(page_id: str, title: str, content: str, parent_id: Optional[str] = None) -> str:
    """更新Confluence页面"""
    return confluence_tools.update_page(page_id, title, content, parent_id)

# 工具：删除Confluence页面
@mcp.tool(
    name="confluence_delete_page",
    description="删除Confluence页面",
    tags=["confluence", "write"]
)
def confluence_delete_page(page_id: str) -> str:
    """删除Confluence页面"""
    return confluence_tools.delete_page(page_id)

# 工具：添加Confluence评论
@mcp.tool(
    name="confluence_add_comment",
    description="向Confluence页面添加评论",
    tags=["confluence", "write"]
)
def confluence_add_comment(page_id: str, content: str) -> str:
    """添加Confluence评论"""
    return confluence_tools.add_comment(page_id, content)

# 工具：获取Confluence子页面
@mcp.tool(
    name="confluence_get_page_children",
    description="获取Confluence页面的子页面",
    tags=["confluence", "read"]
)
def confluence_get_page_children(parent_id: str, limit: int = 25, start: int = 0) -> str:
    """获取子页面"""
    return confluence_tools.get_page_children(parent_id, limit, start)

# 工具：获取Confluence页面标签
@mcp.tool(
    name="confluence_get_page_labels",
    description="获取Confluence页面的标签",
    tags=["confluence", "read"]
)
def confluence_get_page_labels(page_id: str) -> str:
    """获取页面标签"""
    return confluence_tools.get_page_labels(page_id)

# 工具：添加Confluence页面标签
@mcp.tool(
    name="confluence_add_page_label",
    description="向Confluence页面添加标签",
    tags=["confluence", "write"]
)
def confluence_add_page_label(page_id: str, label_name: str) -> str:
    """添加页面标签"""
    return confluence_tools.add_page_label(page_id, label_name)

