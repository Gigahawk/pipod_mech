import cadquery as cq
from cadquery.selectors import BoxSelector

screen_height = 38.95
screen_width = 51.30
screen_thickness = 3.40
screen_lip_depth = 0.6
screen_lip_inset = screen_width - 46.25

active_offset = 3.5
stp_active_offset_x = 2.6
stp_active_offset_y = 1.6
stp_width = 48
stp_height = 34.8
stp_thickness = 2

padding_thickness = 1.00
padding_offset = 1.4
padding_tab_width = 3.00
padding_tab_length = 1.95
padding_tab_fillet = 1.00

total_thickness = screen_thickness + padding_thickness

# Top left (Looking at front of display)
hole_dia1 = 3.10
hole_width1 = 4.8  # width of block
hole_x_offset1 = 2.75
hole_y_offset1 = 5.50

# Bottom left
hole_dia2 = 2.90
hole_width2 = 5.30
hole_x_offset2 = 2.75
hole_y_offset2 = 3.00

# Bottom right
hole_dia3 = 3.10
hole_width3 = 3.90
hole_y_offset3 = 2.00
hole_x_offset3 = 1.80

cable_cutout_width = 25.0
cable_cutout_offset = 6.0  # Distance from top of display to cable edge
cable_cutout_ofst = screen_height/2 - cable_cutout_width/2 - cable_cutout_offset
cable_cutout_depth = 1.0

component_cutout_dims = [
    # Button
    (
     (1.8, -2.6),  # Position
     (6.3, 4.5),   # Dimensions
     2.1,          # Depth
     ),
    # SMC LED
    (
     (-4.1, 13.8),
     (3.7, 1.4),
     1
     ),
    # DAC
    (
     (-22.0, 3.6),
     (13.0, 11.4),
     1.6
     )
    ]


result = (
    cq.Workplane("XY").tag("base_plane")
    .box(
        screen_width, screen_height, screen_thickness,
        centered=[True, True, False])
    .faces(">Z").workplane().tag("interface_plane")
    .center(-padding_offset/2, 0)
    .box(
        screen_width + padding_offset, screen_height, padding_thickness,
        centered=[True, True, False])
    .edges("|Z and <X and <Y").fillet(padding_offset)
    .faces(">Z").workplane().tag("back_plane")
    .workplaneFromTagged("interface_plane")
    .center((screen_width - padding_tab_width)/2, -screen_height/2)
    .box(
        padding_tab_width, padding_tab_length*2, padding_thickness,
        centered=[True, True, False])
    .edges("|Z and <Y").fillet(padding_tab_fillet)
    .workplaneFromTagged("base_plane")
    .center(-screen_width/2, -(screen_height/2 - hole_y_offset1))
    .box(
        hole_x_offset1*2, hole_width1, total_thickness,
        centered=[True, True, False])
    .center(-hole_x_offset1, 0)
    .circle(hole_dia1/2).cutThruAll()
    .workplaneFromTagged("base_plane")
    .center(-screen_width/2, (screen_height/2 - hole_y_offset2))
    .box(
        hole_x_offset2*2, hole_width2, total_thickness,
        centered=[True, True, False])
    .center(-hole_x_offset2, 0)
    .circle(hole_dia2/2).cutThruAll()
    .workplaneFromTagged("base_plane")
    .center(screen_width/2 - hole_width3/2, screen_height/2)
    .box(
        hole_width3, hole_y_offset3*2, total_thickness,
        centered=[True, True, False])
    .center(hole_width3/2 - hole_x_offset3, hole_y_offset3)
    .circle(hole_dia3/2).cutThruAll()
    .workplaneFromTagged("base_plane")
    .center(-screen_width/2, screen_height/2)
    .rect(-100, -screen_height, centered=False).cutBlind(screen_lip_depth)
    .workplaneFromTagged("base_plane")
    .center(screen_width/2 - screen_lip_inset, -screen_height/2)
    .rect(100, 100, centered=False).cutBlind(screen_lip_depth)
    .workplaneFromTagged("base_plane")
    .center(
        -screen_width/2 + active_offset - stp_active_offset_x,
        -screen_height/2 + active_offset - stp_active_offset_y)
    .rect(stp_width, stp_height, centered=False).cutBlind(stp_thickness)
    .workplaneFromTagged("base_plane")
    .center(
        -screen_width/2 + active_offset - stp_active_offset_x,
        -screen_height/2 + active_offset - stp_active_offset_y)
    .rect(
        stp_width + 100,
        stp_height,
        centered=False).cutBlind(stp_thickness/1.5)
    .workplaneFromTagged("base_plane")
    .center(screen_width/2, -cable_cutout_ofst)
    .rect(
        -cable_cutout_depth,
        cable_cutout_width,
        centered=[False, True]).cutThruAll()
)

for cd in component_cutout_dims:
    position, dims, depth = cd
    result = result.workplaneFromTagged("back_plane").center(*position).rect(*dims).cutBlind(-depth)