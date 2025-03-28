
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

Okay, let's analyze the task examples.

## Perception

1.  **Input Structure**: Each input grid is mostly white (0), containing exactly two single pixels of non-white colors.
2.  **Output Structure**: Each output grid is also mostly white but contains two larger shapes, each made of one of the colors from the input pixels.
3.  **Color Preservation**: The colors of the two non-white pixels in the input are used to construct the two shapes in the output. No new colors are introduced.
4.  **Shape Generation**: The shapes generated in the output appear to be identical: a 5x5 "plus" sign or cross.
5.  **Positional Relationship**:
    *   The two input pixels lie either on the same row or the same column.
    *   The two output shapes are positioned symmetrically relative to the midpoint between the original two input pixels.
    *   If the input pixels are in the same row, the shapes are placed side-by-side horizontally, mirrored across the vertical line halfway between the input pixels' columns. Their row coordinate is the same as the input pixels' row.
    *   If the input pixels are in the same column, the shapes are placed one above the other vertically, mirrored across the horizontal line halfway between the input pixels' rows. Their column coordinate is the same as the input pixels' column.
6.  **Midpoint Calculation**: The center of symmetry seems to be exactly halfway between the two input pixels. Since grid coordinates are integers, if the midpoint coordinate is fractional (e.g., 6.5), the two shapes are centered on the two integer coordinates flanking the fractional midpoint (e.g., 6 and 7).
7.  **Shape Details**: The "plus" shape consists of a 5-pixel horizontal line and a 5-pixel vertical line intersecting at their centers.

## Facts (YAML)


```yaml
task_description: Create two mirrored 5x5 plus shapes based on the colors and positions of two input pixels.

elements:
  - element: grid
    properties:
      - type: 2D array of integers (0-9)
      - background_color: white (0)
  - element: input_pixel
    count: 2
    properties:
      - color: non-white
      - size: 1x1
      - role: markers for shape generation and positioning
  - element: output_shape
    count: 2
    properties:
      - shape_type: plus_sign (5x5)
      - color: derived from one of the input_pixels
      - size: 9 pixels each (5 horizontal + 5 vertical - 1 overlap)
      - position: determined by midpoint and orientation of input_pixels

relationships:
  - type: input_pixel_alignment
    condition: The two input_pixels always share either the same row or the same column coordinate.
  - type: color_mapping
    description: Each output_shape inherits the color of one unique input_pixel.
  - type: positioning
    description: >
      The two output_shapes are positioned symmetrically around the midpoint
      between the two input_pixels.
    details:
      - if input_pixels are horizontally aligned (same row):
          midpoint_column = (col1 + col2) / 2
          center1_col = floor(midpoint_column)
          center2_col = ceil(midpoint_column)
          center_row = row1 (which equals row2)
          Shape 1 centered at (center_row, center1_col)
          Shape 2 centered at (center_row, center2_col)
      - if input_pixels are vertically aligned (same column):
          midpoint_row = (row1 + row2) / 2
          center1_row = floor(midpoint_row)
          center2_row = ceil(midpoint_row)
          center_col = col1 (which equals col2)
          Shape 1 centered at (center1_row, center_col)
          Shape 2 centered at (center2_row, center_col)
  - type: reflection
    description: >
      The two output_shapes are reflections of each other across the axis
      defined by the midpoint between the input_pixels.

actions:
  - action: find_pixels
    input: input_grid
    output: coordinates (r1, c1), (r2, c2) and colors color1, color2 of the two non-white pixels.
  - action: determine_orientation_and_midpoint
    input: pixel coordinates (r1, c1), (r2, c2)
    output: orientation ('horizontal' or 'vertical'), midpoint coordinates (mid_r, mid_c)
  - action: calculate_shape_centers
    input: orientation, midpoint coordinates, original coordinates
    output: center coordinates (cr1, cc1), (cr2, cc2) for the two shapes.
  - action: draw_shapes
    input: output_grid, shape_centers (cr1, cc1), (cr2, cc2), colors color1, color2
    output: modified output_grid with two 5x5 plus shapes drawn.

constants:
  - name: shape_pattern
    value: 5x5 plus sign
    definition: A central pixel plus the 2 pixels above, below, left, and right it, AND the 2 pixels further above, below, left and right. Alternatively, a 1x5 horizontal line and a 5x1 vertical line intersecting at their centers.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Scan the input grid to find the coordinates and colors of the two non-white pixels. Let them be (r1, c1) with color1 and (r2, c2) with color2.
3.  Determine the alignment of the input pixels:
    *   If r1 equals r2, the alignment is horizontal.
    *   If c1 equals c2, the alignment is vertical.
4.  Calculate the center coordinates for the two output shapes based on the alignment:
    *   If alignment is horizontal:
        *   The center row for both shapes is r1.
        *   Calculate the midpoint column: mid_c = (c1 + c2) / 2.
        *   The center column for the first shape (using color1) is floor(mid_c).
        *   The center column for the second shape (using color2) is ceil(mid_c).
    *   If alignment is vertical:
        *   The center column for both shapes is c1.
        *   Calculate the midpoint row: mid_r = (r1 + r2) / 2.
        *   The center row for the first shape (using color1) is floor(mid_r).
        *   The center row for the second shape (using color2) is ceil(mid_r).
5.  Define the "5x5 plus" shape relative to a center coordinate (cr, cc): The shape occupies pixels (cr, cc-2), (cr, cc-1), (cr, cc), (cr, cc+1), (cr, cc+2) and (cr-2, cc), (cr-1, cc), (cr, cc), (cr+1, cc), (cr+2, cc).
6.  Draw the first 5x5 plus shape onto the output grid using color1, centered at its calculated center coordinates. Ensure drawing stays within grid boundaries.
7.  Draw the second 5x5 plus shape onto the output grid using color2, centered at its calculated center coordinates. Ensure drawing stays within grid boundaries.
8.  Return the completed output grid.
