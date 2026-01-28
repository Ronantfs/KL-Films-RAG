from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("film-listings")


@mcp.tool(
    name="is_film_showing",
    description="Check if a specific film is showing at a cinema on a given date",
)
def is_film_showing(cinema: str, date: str, film_title: str) -> Dict[str, Any]:
    return {
        "showing": False,
        "cinema": cinema,
        "date": date,
        "film_title": film_title,
    }


@mcp.tool(
    name="list_films_at_cinema",
    description="List all films playing at a cinema on a given date",
)
def list_films_at_cinema(cinema: str, date: str) -> Dict[str, Any]:
    return {
        "cinema": cinema,
        "date": date,
        "films": [],
    }


if __name__ == "__main__":
    # This is now a pure MCP server
    mcp.run()
