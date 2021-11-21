import base64
from collections import defaultdict

from dash import html


def read_rows(rows):
    def format_group_range_descriptions(row):
        range_descriptions = [
            range_description.strip()
            for range_description in row["group_data"].split(",")
        ]
        row_data = defaultdict(list)
        for range_description in range_descriptions:
            second_type_description, second_range_description = range_description.split(
                " "
            )
            row_data[second_type_description].append(
                [int(x) for x in second_range_description.split("-")]
            )
        return [row["group_name"], row_data]

    return [format_group_range_descriptions(row) for row in rows]


def format_svg(dwg):
    raw_content = dwg.tostring()
    content = str(base64.b64encode(raw_content.encode("utf-8")), "utf-8")
    data_uri = "data:image/svg+xml;base64,{}".format(content)
    return html.Div(
        html.A(
            [
                "(click to download full size image)",
                html.Img(src=data_uri, style={"width": "110cm", "height": "32cm"}),
            ],
            href=data_uri,
            target="_blank",
            download="stripes.svg",
        ),
    )
