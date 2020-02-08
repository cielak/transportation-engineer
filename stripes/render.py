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
                svgwrite.shapes.Line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
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
            gr.add(
                svgwrite.shapes.Line(
                    **line_defaults, start=(x + w / 2, y), end=(x, y + h / 2)
                )
            )
            gr.add(
                svgwrite.shapes.Line(
                    **line_defaults, start=(x + w, y + h / 2), end=(x + w / 2, y + h)
                )
            )
        else:
            raise ValueError("Unknown signal second type")
        return gr

    def green_length_annotations(self, seconds):
        starts = []
        ends = []
        last = None
        for i, s in enumerate(seconds + [None]):
            if s == SecondType.green and last != SecondType.green:
                starts.append(i)
            if last == SecondType.green and s != SecondType.green:
                ends.append(i)
            last = s
        greens = [(st, en, en - st) for st, en in zip(starts, ends)]
        if seconds[0] == seconds[-1] and seconds[0] == SecondType.green:
            first_start, first_end, first_len = greens[0]
            last_start, last_end, last_len = greens[-1]
            greens = greens[1:-1] + [(last_start, first_end, first_len + last_len)]
        return greens

    def render_group(self, group):
        w, h = self.second_size
        dwg = svgwrite.Drawing()
        paragraph = dwg.g(font_size=6)
        paragraph.add(dwg.text(group.name, insert=(0, 9)))
        last_type = group.seconds[-1]
        l_place = None
        for i, second in enumerate(group.seconds + [None]):
            x, y = (20 + 5 * i, 0)
            if second:
                paragraph.add(self.render_second(second, insert=(x, y + 5)))
            tick_delta = 4 if i % 5 else 3
            paragraph.add(
                dwg.line(stroke="black", start=(x, y + tick_delta), end=(x, y + 5))
            )
            if second and last_type != second:
                paragraph.add(dwg.text(str(i), insert=(x, y + 3), font_size=4))
                paragraph.add(
                    dwg.line(stroke="black", start=(x, y + 10), end=(x, y + 5))
                )
            last_type = second
            if (second == SecondType.yellow and l_place != SecondType.yellow) or (
                second == SecondType.red_yellow and l_place != SecondType.red_yellow
            ):
                yl_start = (x, y + h + 5)
            if (l_place == SecondType.yellow and second != SecondType.yellow) or (
                l_place == SecondType.red_yellow and second != SecondType.red_yellow
            ):
                yl_end = (x, y + 5)
                paragraph.add(dwg.line(stroke="black", start=yl_start, end=yl_end))
            if second == SecondType.green and l_place != SecondType.green:
                gr_start = (x + 1, y + 9)
                gir_start_i = i
            l_place = second

        for gr_start_i, gr_end_i, gr_len in self.green_length_annotations(
            group.seconds
        ):
            gr_insert_i = (
                (gr_start_i + gr_end_i) / 2 if gr_start_i < gr_end_i else gr_end_i / 2
            )
            gr_insert = (20 + gr_insert_i * w, 9)
            annotation = dwg.text(
                str(gr_len),
                insert=gr_insert,
                fill="white",
                font_size=4,
                font_weight="bold",
            )
            paragraph.add(annotation)

        paragraph.add(
            dwg.rect(
                fill="none",
                stroke="black",
                insert=(20, 5),
                size=(len(group.seconds) * 5, 5),
            )
        )
        return paragraph

    def render_program(self, program):
        scale = 3
        group_height = 11
        left_margin = 5

        sec_w, sec_h = self.second_size
        max_len = max(len(g.seconds) for g in program.groups)
        dwg = svgwrite.Drawing(
            size=(
                scale * (10 + 5 + 20 + 10 + 5 * (1 + max_len)),
                scale * (20 + len(program.groups) * group_height),
            )
        )
        prog = dwg.g(id="program-stripes", stroke_width=0.5)
        for i in range(max_len + 1):
            x = 20 + left_margin + i * sec_w
            y = 10
            if i < max_len:
                prog.add(
                    dwg.line(
                        stroke="black",
                        stroke_width=0.5,
                        start=(x, y),
                        end=(x + sec_w, y),
                    )
                )
            prog.add(dwg.line(stroke="black", start=(x, y), end=(x, y + 3)))
            if i % 5 == 0:
                prog.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                prog.add(dwg.text(str(i), insert=(x - 1, y - 5), font_size=4))
            if i == max_len and i % 5 != 0:
                prog.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                end_txt = dwg.text(str(i), insert=(x + 2, y), font_size=4)
                prog.add(end_txt)
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr.translate(left_margin, 15 + group_height * i)
            prog.add(gr)
        prog.scale(scale)
        dwg.add(prog)
        return dwg
