import sqlite3
from mcp.server.fastmcp import FastMCP
from pathlib import Path


DB_PATH = "./data/olist.sqlite"


mcp_server = FastMCP("SQL MCP", json_response=True)


@mcp_server.resource("schema://tables")
def describe_db() -> dict:
    """
    MCP Resource: Lists all table names in the E-commerce dataset by Olist SQLite database.

    **URI**: `schema://tables`

    **Purpose**: Provides the first step for database schema discovery, returning
    all available table names for the agent to explore further.

    **Returns**:
        dict: JSON-serializable response with:
        - `fail` (bool): False on success, True on error
        - `data` (list): List of dicts containing `{"name": "table_name"}` on success
        - `error_message` (str): Error details if `fail=True`
    """
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if cursor.description is None:
            return dict(fail=True, error_message="Query did not return results")
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return dict(
            fail=False,
            data=rows,
        )
    except Exception as e:
        return dict(
            fail=True,
            error_message=f"Error executing query: {e}",
        )


@mcp_server.resource("schema://{table_name}")
def describe_table(table_name: str) -> dict:
    """
    MCP Resource: Returns detailed schema information for a specific database table.

    **URI**: `schema://{table_name}`

    **Purpose**: Provides complete table structure including CREATE statement and
    column metadata (name, type, nullability, primary key status) for query planning.

    **Args**:
        table_name (str): Name of the table to inspect

    **Returns**:
        dict: JSON-serializable response with:
        - `fail` (bool): False on success, True on error
        - `data` (dict): Contains:
            - `create_statement` (str): Original SQL CREATE TABLE statement
            - `columns` (list): List of column metadata dicts
        - `error_message` (str): Error details if `fail=True`
    """
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
        )
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Table {table_name} not found")
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_res = [
            {
                "name": col[1],
                "type": col[2],
                "notnull": bool(col[3]),
                "pk": bool(col[4]),
            }
            for col in columns
        ]
        conn.close()
        return dict(
            fail=False,
            data={
                "create_statement": result[0],
                "columns": col_res,
            },
        )
    except Exception as e:
        return dict(
            fail=True,
            error_message=f"Error executing query: {e}",
        )


@mcp_server.tool()
def run_sqlite_query(query: str) -> dict:
    """
    MCP Tool: Safely executes SELECT queries against the E-commerce dataset by Olist SQLite database.

    **Security**: Read-only enforcement - rejects INSERT, UPDATE, DELETE, DROP, etc.

    **Args**:
        query (str): SQL SELECT query to execute

    **Returns**:
        dict: JSON-serializable response with:
        - `fail` (bool): False on success, True on error
        - `data` (list): List of row dicts with column names as keys on success
        - `error_message` (str): Error details if `fail=True`
    """
    try:
        # Only allow SELECT queries
        if not query.strip().upper().startswith("SELECT"):
            return dict(fail=True, error_message="Only SELECT queries are allowed")
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description is None:
            return dict(fail=True, error_message="Query did not return results")
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return dict(
            fail=False,
            data=rows,
        )
    except Exception as e:
        return dict(
            fail=True,
            error_message=f"Error executing query: {e}",
        )


if __name__ == "__main__":
    """
    Runs the SQLite MCP server in stdio transport mode.

    Usage: `uv run sqlite_mcp_server.py`

    The server exposes:
    - Resources: schema://tables, schema://{table_name}
    - Tool: run_sqlite_query.
    """
    mcp_server.run(transport="stdio")
