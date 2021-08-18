import cadquery as cq

base_width = 5.7
base_length = 30.4
base_height = 1.5

raised_length = 24.0
raised_height = 1.0

lip_width = 3.9
lip_length = 22.8
lip_height = 0.4
lip_radius = 1.0

# Distance from lip top to base bottom
_lip_offset = 5.1
lip_offset = 2*_lip_offset - lip_width - base_width

hole_dia = 1.4
hole_distance = 27.0

# Distance from hole top to base top
_hole_offset = 1.3
hole_offset = (base_width - hole_dia)/2 - _hole_offset

result = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .faces(">Z").workplane().tag("base_plane")
    .box(raised_length, base_width, raised_height)
    .faces(">Z").workplane().center(0, lip_offset)
    .box(lip_length, lip_width, lip_height)
    .edges("|Z").edges(">Z").fillet(lip_radius)
    .workplaneFromTagged("base_plane").center(hole_distance/2, hole_offset)
    .circle(hole_dia/2).cutThruAll()
    .workplaneFromTagged("base_plane").center(-hole_distance/2, hole_offset)
    .circle(hole_dia/2).cutThruAll()

)