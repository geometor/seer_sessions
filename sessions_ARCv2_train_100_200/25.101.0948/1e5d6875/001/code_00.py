import copy
import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on identified L-shapes of gray (5) or red (2) pixels.

    1.  Find all 3-pixel L-shapes (color 5 or 2) adjacent to a background pixel (7)
        such that the L-shape and the background pixel form a 2x2 square.
    2.  Identify the L-shape's color, its corner pixel 'C' (diagonally opposite the background pixel 'MP' in the 2x2),
        and the coordinates of C=(r,c) and MP=(mr, mc).
    3.  Process Gray L-shapes (color 5):
        - If MP is above C (mr < r):
            - Add pixels relative to MP: Y(4)@MP, Y(4)@MP+(-1,0).
            - Add G(3)@MP+(0,+1) and G(3)@MP+(+1,+1) if C=(r,c) has r=odd and c=odd.
            - Otherwise, add Y(4)@MP+(0,+1) and Y(4)@MP+(+1,+1).
        - If MP is below C (mr > r):
            - Add pixels relative to MP: Y(4)@MP, Y(4)@MP+(-1,-1), Y(4)@MP+(0,-1), Y(4)@MP+(+1,0).
    4.  Process Red L-shapes (color 2):
        - Based on the parity of the corner pixel C=(r,c):
            - If r=even, c=even: Add G(3) at C+(+1,+1).
            - If r=odd, c=odd: Add G(3) at C+(+1,+1). # Tentative based on (even,even) symmetry
            - If r=even, c=odd: Add a G(3) L-shape with pixels C+(0,-1), C+(+1,-1), C+(+1,0).
            - If r=odd, c=even: Add a G(3) L-shape with pixels C+(-1,0), C+(-1,+1), C+(0,+1).
    5.  Added pixels only replace the background color (7).
    """

    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 7
    gray = 5
    red = 2
    yellow = 4
    green = 3

    def is_valid(r, c):
        return 0 <= r < height and 0 <= c < width

    def add_pixel(grid, r, c, color):
        # Safely add a pixel if the location is valid and is background
        if is_valid(r, c) and grid[r][c] == background_color:
            grid[r][c] = color

    # Find L-shapes
    l_shapes = []
    for r in range(height - 1):
        for c in range(width - 1):
            # Coordinates of the 2x2 square
            coords = [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]
            # Colors in the 2x2 square
            colors = [input_grid[rr][cc] for rr, cc in coords]

            non_bg_colors = [color for color in colors if color != background_color]

            # Check for 3 identical non-background pixels (gray or red) and 1 background pixel
            if len(non_bg_colors) == 3 and len(set(non_bg_colors)) == 1:
                shape_color = non_bg_colors[0]
                if shape_color == gray or shape_color == red:
                    mp_coord = None
                    shape_pixels = []
                    corner_coord = None

                    # Find the background pixel (MP) and the shape pixels
                    for i in range(4):
                        if colors[i] == background_color:
                            mp_coord = coords[i]
                        else:
                            shape_pixels.append(coords[i])

                    # Find the corner pixel (C) - diagonally opposite MP
                    if mp_coord == (r, c): corner_coord = (r + 1, c + 1)
                    elif mp_coord == (r + 1, c): corner_coord = (r, c + 1)
                    elif mp_coord == (r, c + 1): corner_coord = (r + 1, c)
                    elif mp_coord == (r + 1, c + 1): corner_coord = (r, c)

                    l_shapes.append({
                        "color": shape_color,
                        "pixels": shape_pixels,
                        "C": corner_coord,
                        "MP": mp_coord
                    })

    # Process L-shapes
    for shape in l_shapes:
        color = shape["color"]
        cr, cc = shape["C"]
        mr, mc = shape["MP"]

        if color == gray:
            # Determine orientation based on MP relative to C
            if mr < cr:  # MP is above C
                use_green = (cr % 2 != 0 and cc % 2 != 0) # Check if C is odd, odd
                secondary_color = green if use_green else yellow

                # Add pixels based on Pattern A
                add_pixel(output_grid, mr, mc, yellow)             # MP
                add_pixel(output_grid, mr - 1, mc, yellow)         # MP+(-1,0)
                add_pixel(output_grid, mr, mc + 1, secondary_color) # MP+(0,+1)
                add_pixel(output_grid, mr + 1, mc + 1, secondary_color) # MP+(+1,+1)

            elif mr > cr: # MP is below C
                 # Add pixels based on Pattern B
                add_pixel(output_grid, mr, mc, yellow)          # MP
                add_pixel(output_grid, mr - 1, mc - 1, yellow)  # MP+(-1,-1)
                add_pixel(output_grid, mr, mc - 1, yellow)      # MP+(0,-1)
                add_pixel(output_grid, mr + 1, mc, yellow)      # MP+(+1,0)
            # Cases mr == cr shouldn't happen if MP is above or below C

        elif color == red:
            # Determine action based on parity of corner C=(cr, cc)
            is_r_even = (cr % 2 == 0)
            is_c_even = (cc % 2 == 0)

            if is_r_even and is_c_even:
                # Rule: C=(even, even) -> Add G at C+(+1,+1)
                add_pixel(output_grid, cr + 1, cc + 1, green)
            elif not is_r_even and not is_c_even:
                 # Rule: C=(odd, odd) -> Add G at C+(+1,+1) (Tentative)
                add_pixel(output_grid, cr + 1, cc + 1, green)
            elif is_r_even and not is_c_even:
                 # Rule: C=(even, odd) -> Add G L-shape opening Top-Right
                 # Pixels: C+(0,-1), C+(+1,-1), C+(+1,0)
                 add_pixel(output_grid, cr, cc - 1, green)
                 add_pixel(output_grid, cr + 1, cc - 1, green)
                 add_pixel(output_grid, cr + 1, cc, green)
            elif not is_r_even and is_c_even:
                 # Rule: C=(odd, even) -> Add G L-shape opening Bottom-Left
                 # Pixels: C+(-1,0), C+(-1,+1), C+(0,+1)
                 add_pixel(output_grid, cr - 1, cc, green)
                 add_pixel(output_grid, cr - 1, cc + 1, green)
                 add_pixel(output_grid, cr, cc + 1, green)

    return output_grid