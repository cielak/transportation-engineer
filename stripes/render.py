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
        gr = svgwrite.container.Group(id=second_type.name)
        defaults = {'size': ('5mm', '5mm'), 'insert':insert}
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
        paragraph = dwg.g(font_size='5mm')
        paragraph.add(dwg.text(group.name, ('1mm', '4.5mm')))
        for i, second in enumerate(group.seconds):
            insert=('{}mm'.format(5*i+20), '0mm')
            s = self.render_second(second, insert)
            paragraph.add(s)
        return paragraph

    def render_program(self, program):
        dwg = svgwrite.Drawing()
        for group in program.groups:
            gr = self.render_group(group)
            dwg.add(gr)
        return dwg.tostring()
