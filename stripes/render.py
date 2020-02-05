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
    def render_second(self, second_type, insert=(0, 0)):
        gr = svgwrite.container.Group()
        defaults = {"size": (5, 5), "insert": insert}
        if second_type == SecondType.off:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="gray"))
        elif second_type == SecondType.red:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="red"))
        elif second_type == SecondType.green:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="green"))
        elif second_type == SecondType.yellow:
            gr.add(svgwrite.shapes.Rect(**defaults, fill="yellow"))
        else:
            raise ValueErrorr("Unknown signal second type")
        return gr

    def render_group(self, group):
        dwg = svgwrite.Drawing()
        paragraph = dwg.g(font_size=6)
        paragraph.add(dwg.text(group.name, insert=(0, 9)))
        last_type = group.seconds[-1]
        for i, second in enumerate(group.seconds):
            x, y = (20 + 5 * i, 0)
            paragraph.add(self.render_second(second, insert=(x, y + 5)))
            paragraph.add(dwg.line(stroke="black", start=(x, y + 10), end=(x, y + 5)))
            if last_type != second:
                paragraph.add(dwg.text(str(i), insert=(x, y + 3), font_size=4))
                paragraph.add(
                    dwg.line(stroke="black", start=(x, y + 4), end=(x, y + 5))
                )
            last_type = second
        return paragraph

    def render_program(self, program):
        dwg = svgwrite.Drawing(size=(200 * 5, 200))
        for i in range(1 + max(len(g.seconds) for g in program.groups)):
            x = 25 + i * 5
            y = 10
            dwg.add(dwg.line(stroke="black", start=(x, y), end=(x + 5, y)))
            dwg.add(dwg.line(stroke="black", start=(x, y), end=(x, y + 3)))
            if i % 5 == 0:
                dwg.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                dwg.add(dwg.text(str(i), insert=(x + 2, y - 2), font_size=5))
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr.translate(5, 20 + 10 * i)
            dwg.add(gr)
        return dwg.tostring()
