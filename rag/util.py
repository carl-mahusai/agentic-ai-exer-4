import re

def split_into_sections(text: str) -> list[tuple[str, str]]:
    """
    Returns

    [
        ("Introduction", "..."),
        ("Naming Conventions", "..."),
        ("Type Hints", "...")
    ]
    """

    lines = text.splitlines()

    sections = []

    current_heading = "Introduction"
    current_text = []

    heading_pattern = re.compile(r"^[A-Z][A-Za-z0-9\s/&()-]{3,}$")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if heading_pattern.match(line):

            if current_text:
                sections.append(
                    (
                        current_heading,
                        "\n".join(current_text)
                    )
                )

            current_heading = line
            current_text = []

        else:
            current_text.append(line)

    if current_text:
        sections.append(
            (
                current_heading,
                "\n".join(current_text)
            )
        )

    return sections