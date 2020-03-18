from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Rect, Line
from svgwrite.text import Text

from stripes.models import SecondType


class TextTemplate:
    def render_second(self, second_type):
        return second_type.name

    def render_group(self, group):
        return group.name, [self.render_second(s) for s in group.seconds]

    def render(self, program):
        return str([self.render_group(g) for g in program.groups])


class SvgRenderer:
    class Drawing(Drawing):
        def append(self, obj):
            self.add(obj)

    class Group(Group):
        def append(self, obj):
            self.add(obj)

    def rect(self, insert, size, stroke="black", stroke_width=0.5, fill=None):
        return Rect(
            insert=insert,
            size=size,
            stroke=stroke,
            stroke_width=stroke_width,
            fill=fill,
        )

    def line(self, start, end, stroke="black", stroke_width=0.5):
        return Line(start=start, end=end, stroke=stroke, stroke_width=stroke_width)

    def text(self, text, insert, fill="black", font_size=4, font_weight="normal"):
        return Text(
            text=text,
            insert=insert,
            fill=fill,
            font_size=font_size,
            font_weight=font_weight,
        )

    def rotated_text(
        self, text, insert, angle=0, fill="black", font_size=4, font_weight="normal"
    ):
        g = self.Group()
        t = self.text(
            text=text,
            insert=(0, 0),
            fill=fill,
            font_size=font_size,
            font_weight=font_weight,
        )
        t.translate(*insert)
        t.rotate(angle)
        g.append(t)
        return g

    def move(self, obj, x, y):
        obj.translate(x, y)
        return obj


class ColorTemplate:
    def __init__(
        self,
        renderer,
        annotate_greens=True,
        left_offset=0,
        right_offset=0,
        annotations=None,
    ):
        self.renderer = renderer
        self.annotate_greens = annotate_greens
        self.left_offset = left_offset
        self.right_offset = right_offset
        self.annotations = annotations
        self.second_size = (5, 5)
        self.group_height = 11
        self.left_margin = 5

    def render(self, program):
        dwg = self.renderer.Drawing()
        prog = self.render_program(program)
        dwg.append(prog)
        return dwg

    def render_second(self, second_type, insert=(0, 0)):
        gr = self.renderer.Group()
        defaults = {"size": self.second_size, "insert": insert, "stroke": "none"}
        line_defaults = {"stroke": "black", "stroke_width": 0.5}
        x, y = insert
        h, w = self.second_size
        if second_type == SecondType.off:
            gr.append(self.renderer.rect(**defaults, fill="gray"))
            gr.append(
                self.renderer.line(**line_defaults, start=(x + w, y), end=(x, y + h))
            )
            gr.append(
                self.renderer.line(**line_defaults, start=(x, y), end=(x + w, y + h))
            )
        elif second_type == SecondType.red:
            gr.append(self.renderer.rect(**defaults, fill="red"))
            gr.append(
                self.renderer.line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
            )
        elif second_type == SecondType.red_yellow:
            gr.append(self.renderer.rect(insert=insert, size=(w, h / 2), fill="red"))
            gr.append(
                self.renderer.rect(
                    insert=(x, y + h / 2), size=(w, h / 2), fill="yellow"
                )
            )
            gr.append(
                self.renderer.line(
                    **line_defaults, start=(x, y + h / 2), end=(x + w, y + h / 2)
                )
            )
        elif second_type == SecondType.green:
            gr.append(self.renderer.rect(**defaults, fill="green"))
        elif second_type == SecondType.yellow:
            gr.append(self.renderer.rect(**defaults, fill="yellow"))
        elif second_type == SecondType.green_blinking:
            gr.append(self.renderer.rect(size=(w / 2, h), insert=(x, y), fill="white"))
            gr.append(
                self.renderer.rect(size=(w / 2, h), insert=(x + w / 2, y), fill="green")
            )
        elif second_type == SecondType.yellow_blinking:
            gr.append(self.renderer.rect(**defaults, fill="yellow"))
            gr.append(
                self.renderer.line(**line_defaults, start=(x + w, y), end=(x, y + h))
            )
            gr.append(
                self.renderer.line(
                    **line_defaults, start=(x + w / 2, y), end=(x, y + h / 2)
                )
            )
            gr.append(
                self.renderer.line(
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
        g = self.renderer.Group()
        for gr_start_i, gr_end_i, gr_len in self.green_length_annotations(
            group.seconds
        ):
            gr_insert_i = (
                (gr_start_i + gr_end_i) / 2 if gr_start_i < gr_end_i else gr_end_i / 2
            )
            gr_insert = (gr_insert_i * w, 9)
            annotation = self.renderer.text(
                str(gr_len),
                insert=gr_insert,
                fill="white",
                font_size=4,
                font_weight="bold",
            )
            g.append(annotation)
        return g

    def render_group_stripe(self, group):
        w, h = self.second_size
        g = self.renderer.Group()
        last_type = group.seconds[-1]
        l_place = None
        for i, second in enumerate(group.seconds + [None]):
            x, y = (w * i, 0)
            if second:
                g.append(self.render_second(second, insert=(x, y + 5)))
            tick_delta = 4 if i % 5 else 3
            g.append(
                self.renderer.line(
                    stroke="black", start=(x, y + tick_delta), end=(x, y + 5)
                )
            )
            if second and last_type != second:
                if self.left_offset <= i <= len(group.seconds) - self.right_offset:
                    g.append(
                        self.renderer.text(
                            str(i - self.left_offset), insert=(x, y + 3), font_size=4
                        )
                    )
                g.append(
                    self.renderer.line(
                        stroke="black", start=(x, y + 10), end=(x, y + 5)
                    )
                )
            last_type = second
            if second == SecondType.yellow and l_place != SecondType.yellow:
                yl_start = (x, y + h + 5)
            if l_place == SecondType.yellow and second != SecondType.yellow:
                yl_end = (x, y + 5)
                g.append(self.renderer.line(stroke="black", start=yl_start, end=yl_end))
            if second == SecondType.red_yellow and l_place != SecondType.red_yellow:
                ryl_start = (x, y + h + 5)
            if l_place == SecondType.red_yellow and second != SecondType.red_yellow:
                ryl_end = (x, y + 5)
                g.append(
                    self.renderer.line(stroke="black", start=ryl_start, end=ryl_end)
                )
            l_place = second
        g.append(
            self.renderer.rect(
                fill="none",
                stroke="black",
                insert=(0, 5),
                size=(len(group.seconds) * 5, 5),
            )
        )
        if self.annotate_greens:
            g.append(self.render_green_length_annotations(group))
        return g

    def render_group(self, group):
        g = self.renderer.Group()
        stripe = self.render_group_stripe(group)
        stripe = self.renderer.move(stripe, 20, 0)
        g.append(stripe)
        txt = self.renderer.text(group.name, insert=(0, 0), font_size=6)
        txt = self.renderer.move(txt, 0, 9)
        g.append(txt)
        return g

    def top_ruler(self, length):
        ruler = self.renderer.Group()
        sec_w, sec_h = self.second_size
        for i in range(length + 1):
            x = i * sec_w
            y = 0
            if i < length:
                ruler.append(
                    self.renderer.line(
                        stroke="black",
                        stroke_width=0.5,
                        start=(x, y),
                        end=(x + sec_w, y),
                    )
                )
            ruler.append(
                self.renderer.line(stroke="black", start=(x, y), end=(x, y + 3))
            )
            if i % 5 == 0:
                ruler.append(
                    self.renderer.line(stroke="black", start=(x, y), end=(x, y - 4))
                )
                ruler.append(
                    self.renderer.text(str(i), insert=(x - 1, y - 5), font_size=4)
                )
            if i == length and i % 5 != 0:
                ruler.append(
                    self.renderer.line(stroke="black", start=(x, y), end=(x, y - 4))
                )
                end_txt = self.renderer.text(str(i), insert=(x + 2, y), font_size=4)
                ruler.append(end_txt)
        return ruler

    def render_annotations(self, annotations):
        w, h = self.second_size
        g = self.renderer.Group()
        for i, txt in annotations:
            x = (self.left_offset + i) * w
            g.append(
                self.renderer.rotated_text(
                    txt, insert=(x, 0), font_size=h, fill="black", angle=90
                )
            )
            g.append(self.renderer.line(stroke="black", start=(x, -1), end=(x, -6)))
        return g

    def render_program(self, program):
        w, h = self.second_size
        group_height = self.group_height
        left_margin = self.left_margin

        max_len = max(len(g.seconds) for g in program.groups)
        prog = self.renderer.Group()
        top_ruler = self.top_ruler(max_len - self.left_offset - self.right_offset)
        top_ruler = self.renderer.move(
            top_ruler, 20 + left_margin + w * self.left_offset, 10
        )
        prog.append(top_ruler)
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr = self.renderer.move(gr, left_margin, 15 + group_height * i)
            prog.append(gr)
        if self.annotations:
            annotations = self.render_annotations(self.annotations)
            annotations = self.renderer.move(
                annotations, 20 + left_margin, 20 + group_height * len(program.groups)
            )
            prog.append(annotations)
        return prog
