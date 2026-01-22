from mcp.server import MCPServer  # type: ignore

server = MCPServer()


@server.tool()
def search_film(cinema: str | None, dates: list[str] | None, film_title: str | None):
    return {"cinema": cinema, "dates": dates, "film_title": film_title}


if __name__ == "__main__":
    server.run()
