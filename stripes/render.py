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
    def render_second(self, second_type, insert=(0,0)):
        gr = svgwrite.container.Group()
        defaults = {'size': (5, 5), 'insert':insert}
        if second_type == SecondType.off:
            gr.add(svgwrite.shapes.Rect(**defaults, fill='gray'))
        elif second_type == SecondType.red:
            gr.add(svgwrite.shapes.Rect(**defaults, fill='red'))
        elif second_type == SecondType.green:
            gr.add(svgwrite.shapes.Rect(**defaults, fill='green'))
        elif second_type == SecondType.yellow:
            gr.add(svgwrite.shapes.Rect(**defaults, fill='yellow'))
        else:
            raise ValueErrorr('Unknown signal second type')
        return gr

    def render_group(self, group):
        dwg = svgwrite.Drawing()
        paragraph = dwg.g(font_size=4)
        paragraph.add(dwg.text(group.name, insert=(1, 4.5)))
        for i, second in enumerate(group.seconds):
            insert_s=(20+5*i, 0)
            s = self.render_second(second, insert_s)
            paragraph.add(s)
        return paragraph

    def render_program(self, program):
        dwg = svgwrite.Drawing(size=(200*5, 200))
        for i, group in enumerate(program.groups):
            gr = self.render_group(group)
            gr.translate(1, 10+10*i)
            dwg.add(gr)
        return dwg.tostring()
