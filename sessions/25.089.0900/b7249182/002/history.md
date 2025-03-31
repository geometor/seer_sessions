
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 1 1 0 0 0 0
0 0 0 0 0 3 0 0 1 0 0 0 0
0 3 3 3 3 3 0 0 1 1 1 1 1
0 0 0 0 0 3 0 0 1 0 0 0 0
0 0 0 0 0 3 3 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 8 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 5 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**: The task involves identifying two distinct colored pixels in the input grid. These pixels serve as anchors or starting points. The transformation draws two connected "staple" or "U" shapes based on the positions of these two initial pixels. The orientation (horizontal or vertical) and position of the final structure depend on the relative positions of the input pixels. Each initial pixel determines the color and one half of the final structure. The two halves meet near the midpoint between the initial pixels. The structure consists of a line segment drawn from the initial pixel towards the midpoint, a perpendicular line segment of length 5 centered near the midpoint, and a connection between the centers of these perpendicular segments.

*   **Facts (YAML)**:
    
```yaml
    task_description: Draw two connected 'staple' shapes based on two input pixels.
    
    elements:
      - element: background
        color: white (0)
      - element: anchor_pixel
        count: 2
        properties:
          - color: non-white (1-9)
          - position: (row, column)
    
    relationships:
      - type: positional
        description: Two anchor pixels exist in the input grid. Their relative positions (same row or same column) determine the orientation of the output structure.
      - type: midpoint
        description: The center of the output structure is located near the midpoint between the two anchor pixels.
    
    actions:
      - action: identify_pixels
        inputs: input_grid
        outputs: pixel1_coords, pixel1_color, pixel2_coords, pixel2_color
        description: Find the coordinates and colors of the two non-white pixels.
      - action: calculate_midpoint
        inputs: pixel1_coords, pixel2_coords
        outputs: midpoint_row, midpoint_col
        description: Calculate the midpoint coordinates between the two anchor pixels.
      - action: determine_orientation
        inputs: pixel1_coords, pixel2_coords
        outputs: orientation ('horizontal' or 'vertical')
        description: Check if pixels are in the same row or same column.
      - action: define_segments
        inputs: pixel1_coords, pixel1_color, pixel2_coords, pixel2_color, midpoint_row, midpoint_col, orientation
        outputs: segments_to_draw (list of lines/pixels with coords and colors)
        description: >
          Based on orientation and midpoint, define the coordinates for:
          1. Two main segments (perpendicular to the line connecting input pixels), each 5 units long, centered near the midpoint, offset slightly from the midpoint line.
          2. Two connecting segments, drawn from each input pixel to the center of its corresponding main segment.
          3. A bridge segment connecting the centers of the two main segments.
      - action: draw_output
        inputs: input_grid_dimensions, segments_to_draw
        outputs: output_grid
        description: Create an output grid of the same size as the input, initialized to white, and draw the defined segments using their respective colors.
    
    properties_change:
      - property: pixel_count
        change: Increases significantly. The two initial pixels expand into larger shapes.
      - property: structure
        change: Two single pixels transform into two connected, extended shapes ('staples' or 'H-like').
      - property: grid_content
        change: White background is partially filled with colored pixels forming the new structure. Input pixel locations remain part of the structure.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid, but with all pixels set to white (0), maintaining the original dimensions.
    2.  Scan the input grid to find the coordinates (row1, col1) and color (color1) of the first non-white pixel (P1).
    3.  Scan the input grid to find the coordinates (row2, col2) and color (color2) of the second non-white pixel (P2).
    4.  Calculate the midpoint row `mr = (row1 + row2) / 2` and midpoint column `mc = (col1 + col2) / 2`.
    5.  **If** the input pixels are in the same row (row1 == row2) (Horizontal orientation):
        a.  Determine the center row for the vertical segments: `vr = round(mr) = row1`.
        b.  Determine the center column for P1's vertical segment: `vc1 = floor(mc - 0.5)`.
        c.  Determine the center column for P2's vertical segment: `vc2 = ceil(mc + 0.5)`.
        d.  Draw P1's vertical segment: Color pixels from `(vr - 2, vc1)` to `(vr + 2, vc1)` with `color1`.
        e.  Draw P2's vertical segment: Color pixels from `(vr - 2, vc2)` to `(vr + 2, vc2)` with `color2`.
        f.  Draw P1's horizontal segment: Color pixels from `(vr, col1)` to `(vr, vc1)` with `color1`.
        g.  Draw P2's horizontal segment: Color pixels from `(vr, vc2)` to `(vr, col2)` with `color2`.
        h.  Draw the connection segment: Color pixels from `(vr, vc1)` to `(vr, vc2)`. For pixels in this segment where the column index `c <= mc`, use `color1`. For pixels where `c > mc`, use `color2`.
    6.  **Else If** the input pixels are in the same column (col1 == col2) (Vertical orientation):
        a.  Determine the center column for the horizontal segments: `hc = round(mc) = col1`.
        b.  Determine the center row for P1's horizontal segment: `hr1 = floor(mr - 0.5)`.
        c.  Determine the center row for P2's horizontal segment: `hr2 = ceil(mr + 0.5)`.
        d.  Draw P1's horizontal segment: Color pixels from `(hr1, hc - 2)` to `(hr1, hc + 2)` with `color1`.
        e.  Draw P2's horizontal segment: Color pixels from `(hr2, hc - 2)` to `(hr2, hc + 2)` with `color2`.
        f.  Draw P1's vertical segment: Color pixels from `(row1, hc)` to `(hr1, hc)` with `color1`.
        g.  Draw P2's vertical segment: Color pixels from `(hr2, hc)` to `(row2, hc)` with `color2`.
        h.  Draw the connection segment: Color pixels from `(hr1, hc)` to `(hr2, hc)`. For pixels in this segment where the row index `r <= mr`, use `color1`. For pixels where `r > mr`, use `color2`.
    7.  Return the modified output grid.
```python
import numpy as np
import math

"""
This transformation identifies two distinct colored pixels in the input grid.
It then draws two connected 'staple' or 'U' shapes centered around the midpoint 
between these two pixels. The orientation of the staples (horizontal or vertical) 
depends on whether the input pixels share the same row or column.

1. Find the coordinates and colors of the two non-white pixels in the input grid.
2. Calculate the midpoint coordinates between these two pixels.
3. Determine the orientation:
   - If the pixels are in the same row (horizontal orientation):
     - Calculate the center columns for the two vertical 'legs' of the staples, 
       offset horizontally from the midpoint column.
     - Draw two vertical segments (legs) of length 5, centered vertically on the 
       shared row, using the respective pixel colors.
     - Draw two horizontal segments connecting each original pixel to the center 
       of its corresponding vertical leg.
     - Draw a horizontal segment connecting the centers of the two vertical legs, 
       splitting the color at the midpoint column.
   - If the pixels are in the same column (vertical orientation):
     - Calculate the center rows for the two horizontal 'bases' of the staples, 
       offset vertically from the midpoint row.
     - Draw two horizontal segments (bases) of length 5, centered horizontally 
       on the shared column, using the respective pixel colors.
     - Draw two vertical segments connecting each original pixel to the center 
       of its corresponding horizontal base.
     - Draw a vertical segment connecting the centers of the two horizontal bases, 
       splitting the color at the midpoint row.
4. Return the resulting grid.
"""

def find_colored_pixels(grid):
    """Finds all non-background (non-zero) pixels."""
    pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                pixels.append({'row': r, 'col': c, 'color': grid[r, c]})
    return pixels

def draw_pixel(grid, r, c, color):
    """Draws a pixel if within grid bounds."""
    rows, cols = grid.shape
    if 0 <= r < rows and 0 <= c < cols:
        grid[r, c] = color

def draw_vline(grid, r_start, r_end, c, color):
    """Draws a vertical line."""
    for r in range(min(r_start, r_end), max(r_start, r_end) + 1):
        draw_pixel(grid, r, c, color)

def draw_hline(grid, r, c_start, c_end, color):
    """Draws a horizontal line."""
    for c in range(min(c_start, c_end), max(c_start, c_end) + 1):
        draw_pixel(grid, r, c, color)

def transform(input_grid):
    """
    Transforms the input grid by drawing connected staple shapes based on two anchor pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np)

    # Find the two anchor pixels
    pixels = find_colored_pixels(input_np)
    if len(pixels) != 2:
        # Handle unexpected input (e.g., return empty or input grid)
        # For this specific task structure, we expect exactly two points.
        return output_grid.tolist() 

    p1 = pixels[0]
    p2 = pixels[1]
    r1, c1, color1 = p1['row'], p1['col'], p1['color']
    r2, c2, color2 = p2['row'], p2['col'], p2['color']

    # Calculate midpoint (can be float)
    mr = (r1 + r2) / 2.0
    mc = (c1 + c2) / 2.0

    # Determine orientation and draw shapes
    if r1 == r2:  # Horizontal orientation
        vr = r1 # Center row is the shared row
        # Calculate center columns for the vertical segments (staple legs)
        # Centers are offset by 1.5 units from the midpoint column
        vc1 = math.floor(mc - 1) 
        vc2 = math.ceil(mc + 1) 

        # Ensure vc1 and vc2 are distinct if mc is integer or half-integer
        # This adjustment ensures a gap of at least 2, matching examples
        if vc2 - vc1 < 3:
             if mc % 1 == 0: # Integer midpoint
                 vc1 = int(mc - 2)
                 vc2 = int(mc + 2)
             else: # Half-integer midpoint like 6.5
                 vc1 = int(mc - 1.5)
                 vc2 = int(mc + 1.5)
                 
        # Ensure p1 corresponds to vc1 and p2 to vc2 based on column order
        if c1 > c2:
             vc1, vc2 = vc2, vc1 # Swap centers if p1 is to the right of p2
             color1, color2 = color2, color1 # Swap colors too
             r1, r2 = r2, r1 # Swap original coords
             c1, c2 = c2, c1
             
        # Draw vertical segment 1 (length 5)
        draw_vline(output_grid, vr - 2, vr + 2, vc1, color1)
        # Draw vertical segment 2 (length 5)
        draw_vline(output_grid, vr - 2, vr + 2, vc2, color2)

        # Draw horizontal segment 1 (from p1 to center of leg 1)
        draw_hline(output_grid, vr, c1, vc1, color1)
        # Draw horizontal segment 2 (from p2 to center of leg 2)
        draw_hline(output_grid, vr, c2, vc2, color2)

        # Draw connection segment between leg centers, splitting color at midpoint
        for c in range(vc1, vc2 + 1):
            if c <= mc:
                 draw_pixel(output_grid, vr, c, color1)
            else:
                 draw_pixel(output_grid, vr, c, color2)


    elif c1 == c2:  # Vertical orientation
        hc = c1 # Center column is the shared column
        # Calculate center rows for the horizontal segments (staple bases)
        # Centers are offset by 1.5 units from the midpoint row
        hr1 = math.floor(mr - 1)
        hr2 = math.ceil(mr + 1)

        # Ensure hr1 and hr2 are distinct
        if hr2 - hr1 < 3:
             if mr % 1 == 0: # Integer midpoint
                 hr1 = int(mr - 2)
                 hr2 = int(mr + 2)
             else: # Half-integer midpoint like 5.5
                 hr1 = int(mr - 1.5)
                 hr2 = int(mr + 1.5)

        # Ensure p1 corresponds to hr1 and p2 to hr2 based on row order
        if r1 > r2:
            hr1, hr2 = hr2, hr1 # Swap centers if p1 is below p2
            color1, color2 = color2, color1 # Swap colors
            r1, r2 = r2, r1 # Swap original coords
            c1, c2 = c2, c1
            
        # Draw horizontal segment 1 (length 5)
        draw_hline(output_grid, hr1, hc - 2, hc + 2, color1)
        # Draw horizontal segment 2 (length 5)
        draw_hline(output_grid, hr2, hc - 2, hc + 2, color2)

        # Draw vertical segment 1 (from p1 to center of base 1)
        draw_vline(output_grid, r1, hr1, hc, color1)
        # Draw vertical segment 2 (from p2 to center of base 2)
        draw_vline(output_grid, r2, hr2, hc, color2)

        # Draw connection segment between base centers, splitting color at midpoint
        for r in range(hr1, hr2 + 1):
             if r <= mr:
                 draw_pixel(output_grid, r, hc, color1)
             else:
                 draw_pixel(output_grid, r, hc, color2)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
