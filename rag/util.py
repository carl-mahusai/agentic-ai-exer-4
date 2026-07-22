from collections import Counter

import fitz

from rag.models import Document, Section


def split_into_sections(document: Document) -> list[Section]:
    """
    Splits a PDF into semantic sections using font size detection.

    The most common font size is assumed to be body text.
    Any line with a larger font size is treated as a section heading.
    """

    pdf = fitz.open(document.filepath)

    #
    # Pass 1: determine the body font size
    #

    font_sizes = []

    for page in pdf:
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                for span in line["spans"]:
                    font_sizes.append(round(span["size"]))

    body_font_size = Counter(font_sizes).most_common(1)[0][0]

    #
    # Pass 2: build sections
    #

    sections: list[Section] = []

    current_heading = "Introduction"
    current_text = []

    for page in pdf:

        blocks = page.get_text("dict")["blocks"]

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                line_text = ""
                largest_font = 0

                for span in line["spans"]:

                    line_text += span["text"]

                    largest_font = max(
                        largest_font,
                        round(span["size"])
                    )

                line_text = line_text.strip()

                if not line_text:
                    continue

                #
                # Heading
                #

                if largest_font > body_font_size:

                    if current_text:

                        sections.append(
                            Section(
                                heading=current_heading,
                                text="\n".join(current_text)
                            )
                        )

                    current_heading = line_text
                    current_text = []

                #
                # Body text
                #

                else:

                    current_text.append(line_text)

    #
    # Last section
    #

    if current_text:

        sections.append(
            Section(
                heading=current_heading,
                text="\n".join(current_text)
            )
        )

    pdf.close()

    return sections