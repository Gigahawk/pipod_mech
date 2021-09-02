import cadquery as cq
from cadquery.selectors import BoxSelector

# Monkeypatch rounded rect in
def rounded_rect(self, xlen, ylen, fillet_radius):
    rect = cq.Workplane().rect(xlen, ylen).val()
    pts = rect.Vertices()
    rect = rect.fillet2D(fillet_radius, pts)
    return self.eachpoint(lambda loc: rect.moved(loc), True)

cq.Workplane.rounded_rect = rounded_rect

base_width = 5.7
base_length = 30.4
base_height = 1.5

raised_length = 24.0
raised_height = 0.9

lip_width = 3.9
lip_length = 22.8
lip_height = 0.5
lip_radius = 1.0

# Distance from lip top to base bottom
_lip_offset = 5.1
lip_offset = 2*_lip_offset - lip_width - base_width

hole_dia = 1.4
hole_distance = 27.0

# Distance from hole top to base top
_hole_offset = 1.3
hole_offset = (base_width - hole_dia)/2 - _hole_offset

usb_c_offset = lip_offset + 0.2
usb_c_width = 3.3
usb_c_length = 9.2
usb_c_fillet = 1.6
usb_c_chamfer_width = 3.5
usb_c_chamfer_depth = 3

usb_c_chamfer_points = [
    (0, usb_c_chamfer_width),
    (usb_c_chamfer_depth, 0),
    (0, 0)]

result = (
    cq.Workplane("XY").tag("base_plane")
    .box(
        base_length, base_width, base_height, centered=[True, True, False])
    .faces(">Z").workplane()
    .box(
        raised_length, base_width, raised_height, centered=[True, True, False])
    .faces(">Z").workplane().center(0, lip_offset)
    .box(lip_length, lip_width, lip_height, centered=[True, True, False])
    .edges("|Z").edges(">Z").fillet(lip_radius)
    .workplaneFromTagged("base_plane").center(-hole_distance/2, hole_offset)
    .circle(hole_dia/2).cutThruAll()
    .workplaneFromTagged("base_plane").center(hole_distance/2, hole_offset)
    .circle(hole_dia/2).cutThruAll()
    .workplaneFromTagged("base_plane")
    .transformed(
        offset=cq.Vector(-usb_c_length/2, 0, 0), rotate=cq.Vector(0, 90, 0))
    .center(0, usb_c_offset)
    .transformed(rotate=cq.Vector(0, 0, 180))
    .polyline(usb_c_chamfer_points).close().cutBlind(usb_c_length)
    .workplaneFromTagged("base_plane").center(0, usb_c_offset)
    .rounded_rect(usb_c_length, usb_c_width, usb_c_fillet).cutThruAll()
)