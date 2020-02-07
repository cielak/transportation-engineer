import svgwrite

from stripes.models import SecondType


class SimpleRenderer:
    def render_second(self, second_type):
        return second_type.name

    def render_group(self, group):
        return group.name, [self.render_second(s) for s in group.seconds]

    def render_program(self, program):
        return str([self.render_group(g) for g in program.groups])


class SvgRenderer:
    second_size = (5, 5)

    def render_second(self, second_type, insert=(0, 0)):
        gr = svgwrite.container.Group()
        defaults = {"size": self.second_size, "insert": insert}
        line_defaults = {"stroke": "black", "stroke_width": 0.5}
        x, y = insert
        h, w = self.second_size
        if second_type == SecondType.off:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="gray"))
            gr.add(
                svgwrite.shapes.Line(**line_defaults, start=(x + w, y), end=(x, y + h))
            )
            gr.add(
                svgwrite.shapes.Line(**line_defaults, start=(x, y), end=(x + w, y + h))
            )
        elif second_type == SecondType.red:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="red"))
            gr.add(
                svgwrite.shapes.Line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
            )
        elif second_type == SecondType.red_yellow:
            gr.add(svgwrite.shapes.Rect(insert=insert, size=(w, h / 2), fill="red"))
            gr.add(
                svgwrite.shapes.Rect(
                    insert=(x, y + h / 2), size=(w, h / 2), fill="yellow"
                )
            )
            gr.add(
                svgwrite.shapes.Line(**line_defaults, start=(x + w, y), end=(x, y + h))
            )
        elif second_type == SecondType.green:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="green"))
        elif second_type == SecondType.yellow:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="yellow"))
        elif second_type == SecondType.green_blinking:
            gr.add(svgwrite.shapes.Rect(size=(w / 2, h), insert=(x, y), fill="white"))
            gr.add(
                svgwrite.shapes.Rect(
                    size=(w / 2, h), insert=(x + w / 2, y), fill="green"
                )
            )
        elif second_type == SecondType.yellow_blinking:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="yellow"))
            gr.add(
                svgwrite.shapes.Line(**line_defaults, start=(x + w, y), end=(x, y + h))
            )
        else:
            raise ValueError("Unknown signal second type")
        return gr

    def render_group(self, group):
        dwg = svgwrite.Drawing()
        paragraph = dwg.g(font_size=6)
        paragraph.add(dwg.text(group.name, insert=(0, 9)))
        last_type = group.seconds[-1]
        for i, second in enumerate(group.seconds):
            x, y = (20 + 5 * i, 0)
            paragraph.add(self.render_second(second, insert=(x, y + 5)))
            tick_delta = 4 if i % 5 else 3
            paragraph.add(
                dwg.line(stroke="black", start=(x, y + tick_delta), end=(x, y + 5))
            )
            if last_type != second:
                paragraph.add(dwg.text(str(i), insert=(x, y + 3), font_size=4))
                paragraph.add(
                    dwg.line(stroke="black", start=(x, y + 10), end=(x, y + 5))
                )
            last_type = second
        return paragraph

    def render_program(self, program):
        dwg = svgwrite.Drawing(size=(200 * 5, 200))
        for i in range(1 + max(len(g.seconds) for g in program.groups)):
            x = 25 + i * 5
            y = 10
            dwg.add(
                dwg.line(stroke="black", stroke_width=0.5, start=(x, y), end=(x + 5, y))
            )
            dwg.add(dwg.line(stroke="black", start=(x, y), end=(x, y + 3)))
            if i % 5 == 0:
                dwg.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                dwg.add(dwg.text(str(i), insert=(x + 2, y - 2), font_size=5))
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr.translate(5, 20 + 10 * i)
            dwg.add(gr)
        return dwg.tostring()
