import svgwrite
from svgwrite.shapes import Rect, Line
from svgwrite.text import Text

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

    def __init__(
        self, annotate_greens=True, left_offset=0, right_offset=0, annotations=None
    ):
        self.annotate_greens = annotate_greens
        self.left_offset = left_offset
        self.right_offset = right_offset
        self.annotations = annotations

    def _rect(self, insert, size, stroke="black", stroke_width=0.5, fill=None):
        return Rect(
            insert=insert,
            size=size,
            stroke=stroke,
            stroke_width=stroke_width,
            fill=fill,
        )

    def _line(self, start, end, stroke="black", stroke_width=0.5):
        return Line(start=start, end=end, stroke=stroke, stroke_width=stroke_width)

    def _text(self, text, insert, font_size=4):
        return Text(text=text, insert=insert, font_size=font_size)

    def _move(self, obj, x, y):
        obj.translate(x, y)
        return obj

    def render_second(self, second_type, insert=(0, 0)):
        gr = svgwrite.container.Group()
        defaults = {"size": self.second_size, "insert": insert}
        line_defaults = {"stroke": "black", "stroke_width": 0.5}
        x, y = insert
        h, w = self.second_size
        if second_type == SecondType.off:
            gr.add(self._rect(**defaults, fill="gray"))
            gr.add(self._line(**line_defaults, start=(x + w, y), end=(x, y + h)))
            gr.add(self._line(**line_defaults, start=(x, y), end=(x + w, y + h)))
        elif second_type == SecondType.red:
            gr.add(self._rect(**defaults, fill="red"))
            gr.add(
                self._line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
            )
        elif second_type == SecondType.red_yellow:
            gr.add(self._rect(insert=insert, size=(w, h / 2), fill="red"))
            gr.add(self._rect(insert=(x, y + h / 2), size=(w, h / 2), fill="yellow"))
            gr.add(
                self._line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
            )
        elif second_type == SecondType.green:
            gr.add(self._rect(**defaults, fill="green"))
        elif second_type == SecondType.yellow:
            gr.add(self._rect(**defaults, fill="yellow"))
        elif second_type == SecondType.green_blinking:
            gr.add(self._rect(size=(w / 2, h), insert=(x, y), fill="white"))
            gr.add(self._rect(size=(w / 2, h), insert=(x + w / 2, y), fill="green"))
        elif second_type == SecondType.yellow_blinking:
            gr.add(self._rect(**defaults, fill="yellow"))
            gr.add(self._line(**line_defaults, start=(x + w, y), end=(x, y + h)))
            gr.add(
                self._line(**line_defaults, start=(x + w / 2, y), end=(x, y + h / 2))
            )
            gr.add(
                self._line(
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

    def render_green_length_annotations(self, group):
        w, h = self.second_size
        dwg = svgwrite.Drawing()
        g = dwg.g(fill="white", font_size=4, font_weight="bold")
        for gr_start_i, gr_end_i, gr_len in self.green_length_annotations(
            group.seconds
        ):
            gr_insert_i = (
                (gr_start_i + gr_end_i) / 2 if gr_start_i < gr_end_i else gr_end_i / 2
            )
            gr_insert = (gr_insert_i * w, 9)
            annotation = self._text(str(gr_len), insert=gr_insert)
            g.add(annotation)
        return g

    def render_group_stripe(self, group):
        w, h = self.second_size
        dwg = svgwrite.Drawing()
        g = dwg.g()
        last_type = group.seconds[-1]
        l_place = None
        for i, second in enumerate(group.seconds + [None]):
            x, y = (w * i, 0)
            if second:
                g.add(self.render_second(second, insert=(x, y + 5)))
            tick_delta = 4 if i % 5 else 3
            g.add(dwg.line(stroke="black", start=(x, y + tick_delta), end=(x, y + 5)))
            if second and last_type != second:
                if self.left_offset <= i <= len(group.seconds) - self.right_offset:
                    g.add(
                        self._text(
                            str(i - self.left_offset), insert=(x, y + 3), font_size=4
                        )
                    )
                g.add(dwg.line(stroke="black", start=(x, y + 10), end=(x, y + 5)))
            last_type = second
            if second == SecondType.yellow and l_place != SecondType.yellow:
                yl_start = (x, y + h + 5)
            if l_place == SecondType.yellow and second != SecondType.yellow:
                yl_end = (x, y + 5)
                g.add(dwg.line(stroke="black", start=yl_start, end=yl_end))
            if second == SecondType.red_yellow and l_place != SecondType.red_yellow:
                ryl_start = (x, y + h + 5)
            if l_place == SecondType.red_yellow and second != SecondType.red_yellow:
                ryl_end = (x, y + 5)
                g.add(dwg.line(stroke="black", start=ryl_start, end=ryl_end))
            l_place = second
        g.add(
            dwg.rect(
                fill="none",
                stroke="black",
                insert=(0, 5),
                size=(len(group.seconds) * 5, 5),
            )
        )
        if self.annotate_greens:
            g.add(self.render_green_length_annotations(group))
        return g

    def render_group_name(self, group):
        dwg = svgwrite.Drawing()
        g = dwg.g(font_size=6)
        g.add(self._text(group.name, insert=(0, 0)))
        return g

    def render_group(self, group):
        dwg = svgwrite.Drawing()
        g = dwg.g()
        stripe = self.render_group_stripe(group)
        stripe = self._move(stripe, 20, 0)
        g.add(stripe)
        txt = self.render_group_name(group)
        txt = self._move(txt, 0, 9)
        g.add(txt)
        return g

    def top_ruler(self, length):
        dwg = svgwrite.Drawing()
        ruler = dwg.g()
        sec_w, sec_h = self.second_size
        for i in range(length + 1):
            x = i * sec_w
            y = 0
            if i < length:
                ruler.add(
                    dwg.line(
                        stroke="black",
                        stroke_width=0.5,
                        start=(x, y),
                        end=(x + sec_w, y),
                    )
                )
            ruler.add(dwg.line(stroke="black", start=(x, y), end=(x, y + 3)))
            if i % 5 == 0:
                ruler.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                ruler.add(self._text(str(i), insert=(x - 1, y - 5), font_size=4))
            if i == length and i % 5 != 0:
                ruler.add(dwg.line(stroke="black", start=(x, y), end=(x, y - 4)))
                end_txt = self._text(str(i), insert=(x + 2, y), font_size=4)
                ruler.add(end_txt)
        return ruler

    def render_annotations(self, annotations):
        w, h = self.second_size
        dwg = svgwrite.Drawing()
        g = dwg.g(font_size=h, fill="black")
        for i, txt in annotations:
            insert = ((self.left_offset + i) * w, 0)
            text = self._text(txt, insert=insert)
            text.rotate(90, insert)
            g.add(text)
            g.add(dwg.line(stroke="black", start=(insert[0], -1), end=(insert[0], -6)))
        return g

    def render_program(self, program):
        w, h = self.second_size
        scale = 3
        group_height = 11
        left_margin = 5

        max_len = max(len(g.seconds) for g in program.groups)
        dwg = svgwrite.Drawing(
            size=(
                scale * (10 + 5 + 20 + 10 + 5 * (1 + max_len)),
                scale * (20 + len(program.groups) * group_height + 20),
            )
        )
        prog = dwg.g(id="program-stripes", stroke_width=0.5)
        prog.add(dwg.rect(fill="white", size=("100%", "100%"), insert=(0, 0)))
        top_ruler = self.top_ruler(max_len - self.left_offset - self.right_offset)
        top_ruler = self._move(top_ruler, 20 + left_margin + w * self.left_offset, 10)
        prog.add(top_ruler)
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr = self._move(gr, left_margin, 15 + group_height * i)
            prog.add(gr)
        if self.annotations:
            annotations = self.render_annotations(self.annotations)
            annotations = self._move(
                annotations, 20 + left_margin, 20 + group_height * len(program.groups)
            )
            prog.add(annotations)
        prog.scale(scale)
        dwg.add(prog)
        return dwg
