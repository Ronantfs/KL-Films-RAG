def build_context(chunks: list[dict]) -> str:
    lines = []

    for chunk in chunks:
        lines.append(
            f"- {chunk['title']} at {chunk['cinema']} "
            f"(more info: {chunk['url']})"
        )

    return "\n".join(lines)
