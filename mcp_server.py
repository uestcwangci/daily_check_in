# server.py
from mcp.server.fastmcp import FastMCP
from android.wxdushu import DuShuHelper
# Create an MCP server
mcp = FastMCP("WXMcp")
dushu = DuShuHelper("10.0.0.51:5555")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def get_wx_book_list(book_id: str) -> str:
    """Get wx book list"""
    book_data = dushu.get_book_data(book_id)
    return book_data

if __name__ == "__main__":
    mcp.run(transport='sse')