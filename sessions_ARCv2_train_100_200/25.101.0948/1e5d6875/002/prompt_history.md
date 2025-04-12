
## train_1

**input:**
```
7 7 7 7 7 7 7 7
7 7 7 7 2 7 7 7
7 5 7 7 2 2 7 7
7 5 5 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 7 7
```


**output:**
```
7 7 7 7 7 7 7 7
7 7 4 7 2 7 7 7
7 5 4 3 2 2 7 7
7 5 5 3 3 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7
7 7 7 7 2 2 3 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7
7 5 7 7 7 5 5 7
7 5 5 7 7 7 5 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 2 2 7 7 2 7 7
7 7 2 7 7 2 2 7
7 7 7 7 7 7 7 7
```


**output:**
```
7 7 4 7 7 7 7 7
7 5 4 4 7 5 5 7
7 5 5 7 4 4 5 7
7 7 7 7 7 4 7 7
7 7 3 3 7 7 7 7
7 2 2 3 7 2 7 7
7 7 2 7 3 2 2 7
7 7 7 7 3 3 7 7
```

## Perception

The input and output are grids of pixels with different colors. The background color is orange (7). The task involves identifying specific shapes, 3-pixel L-shapes, composed of either gray (5) or red (2) pixels. Based on the color and properties (orientation, location) of these L-shapes, new pixels (yellow 4 and/or green 3) are added to the grid in specific patterns relative to the original L-shapes. The original L-shapes remain unchanged. The rules for adding pixels differ significantly depending on whether the L-shape is gray or red.

## Facts


```yaml
objects:
  - type: grid
    properties:
      background_color: 7 (orange)
  - type: shape
    identifier: L-shape
    properties:
      color: 5 (gray) or 2 (red)
      size: 3 pixels
      connectivity: L-configuration (one pixel connected to two others in the shape)
      corner_pixel: The pixel within the L-shape connected to the other two pixels.
      orientation: Defined by the relative positions of the 3 pixels (e.g., opens Top-Right, Bottom-Right, Bottom-Left, Top-Left).
      missing_pixel (MP): The unique background pixel adjacent to two pixels of the L-shape, which would complete a 2x2 square containing the L-shape.
actions:
  - name: identify_L_shapes
    input: input_grid
    output: list of L-shapes with properties (color, pixels, corner_pixel, orientation, missing_pixel)
  - name: process_gray_L_shape
    input: gray_L_shape (with properties)
    output: set of new pixels (coordinates and colors: Yellow 4, Green 3)
    condition: Based on L-shape orientation.
    details:
      - Fill the Missing Pixel (MP) with Yellow (4).
      - Add 3 more pixels (Yellow or Green) at specific relative positions to MP, determined by the L-shape's orientation.
        - Orientation "opens Top-Right": Add Y at MP+(-1,0), G at MP+(0,+1), G at MP+(+1,+1).
        - Orientation "opens Bottom-Right": Add Y at MP+(-1,-1), Y at MP+(0,-1), Y at MP+(+1,0).
  - name: process_red_L_shape
    input: red_L_shape (with properties)
    output: set of new pixels (coordinates and color: Green 3)
    condition: Based on the parity of the corner_pixel's coordinates (r, c).
    details:
      - If corner (r, c) is (even, even): Add nothing.
      - If corner (r, c) is (odd, odd): Add Green (3) at MP+(+1,+1).
      - If corner (r, c) is (even, odd): Add a Green (3) L-shape (3 pixels) opening Top-Right, with its corner at C+(+1,-1).
      - If corner (r, c) is (odd, even): Add a Green (3) L-shape (3 pixels) opening Bottom-Left, with its corner at C+(-1,+1).
  - name: apply_changes
    input: input_grid, list of new pixels to add
    output: output_grid
    details: Create a copy of the input grid. For each new pixel (coord, color), if the coordinate is within bounds and the current color at that coordinate in the copy is the background color (orange 7), update the color.
relationships:
  - The added pixels' locations and colors depend on the source L-shape's color, orientation, and corner pixel coordinates.
  - Added pixels only replace the background color.
```


## Natural Language Program

1.  **Initialize**: Create a copy of the input grid to serve as the output grid.
2.  **Identify L-Shapes**: Scan the input grid to find all 3-pixel L-shapes made of gray (5) or red (2). For each L-shape, record its color, the coordinates of its three pixels, the coordinate of its corner pixel (C), its orientation (e.g., opens Top-Right, Bottom-Right, etc.), and the coordinate of the background pixel (MP) that would complete its 2x2 bounding box.
3.  **Process Gray L-Shapes**: For each identified gray L-shape:
    a.  Determine its orientation and its Missing Pixel (MP).
    b.  Add Yellow (4) to the output grid at coordinate MP, if MP is currently background (orange 7).
    c.  Based on orientation, determine the coordinates for 3 additional pixels relative to MP:
        i.  If orientation is "opens Top-Right": Target coordinates are MP+(-1,0) [Y], MP+(0,+1) [G], MP+(+1,+1) [G].
        ii. If orientation is "opens Bottom-Right": Target coordinates are MP+(-1,-1) [Y], MP+(0,-1) [Y], MP+(+1,0) [Y].
        iii. (Define rules for other orientations if needed).
    d.  For each target coordinate and its associated color (Y or G) from step 3c, add the color to the output grid at that coordinate, provided it's within bounds and currently background (orange 7).
4.  **Process Red L-Shapes**: For each identified red L-shape:
    a.  Identify its corner pixel C=(r,c) and its Missing Pixel MP.
    b.  Check the parity of the corner pixel's coordinates (r, c).
    c.  Determine the target coordinates and color (Green 3) based on parity:
        i.  If r=even, c=even: No pixels are added.
        ii. If r=odd, c=odd: Target coordinate is MP+(+1,+1). Add Green (3).
        iii. If r=even, c=odd: Target coordinates form a Green (3) L-shape opening Top-Right, with its corner at C+(+1,-1). The three pixels are C+(0,-1), C+(+1,-1), C+(+1,0). Add Green (3) to each.
        iv. If r=odd, c=even: Target coordinates form a Green (3) L-shape opening Bottom-Left, with its corner at C+(-1,+1). The three pixels are C+(-1,0), C+(-1,+1), C+(0,+1). Add Green (3) to each.
    d.  For each target coordinate determined in step 4c, add Green (3) to the output grid at that coordinate, provided it's within bounds and currently background (orange 7).
5.  **Return Output**: The modified grid is the final output.
```python
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
```
