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
    def render_second(self, second_type):
        dwg = svgwrite.Drawing()
        if second_type == SecondType.off:
            pass
        elif second_type == SecondType.red:
            pass
        elif second_type == SecondType.green:
            pass
        return dwg

    def render_group(self, group):
        dwg = svgwrite.Drawing()
        paragraph = dwg.add(dwg.g(font_size=14))
        paragraph.add(dwg.text(group.name, (10, 20)))
        
        return dwg

    def render_program(self, program):
        dwg = svgwrite.Drawing()
        for group in program.groups:
            # gr = self.render_group(group)
            dwg.add(dwg.text(group.name, dx=[10], dy=[50], fill='black'))
        return dwg.tostring()
