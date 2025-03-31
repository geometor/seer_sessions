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