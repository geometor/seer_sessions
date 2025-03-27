
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

Okay, let's analyze the task examples.

**Perception**

1.  **Input/Output Structure:** The output grid is the same size as the input grid. The output grid contains all the pixels from the input grid, plus some additional pixels.
2.  **Key Pattern:** The core transformation seems triggered by a specific horizontal pattern found near the bottom of the input grid. This pattern consists of a central contiguous block of one color (let's call it the "central color") flanked on the left and right by pixels of a different color (the "framing color") within the same row.
3.  **Added Pixels:** New pixels are added to the output grid.
    *   The *color* of the added pixels is always the "central color" from the identified pattern row.
    *   The *location* of the added pixels depends on the location of the "framing color" pixels in the pattern row.
4.  **Location Logic:** For each pixel of the "framing color" in the pattern row (at `R_source, c_frame`), a new pixel is added.
    *   The *column* of the new pixel is the same as the framing pixel's column (`c_frame`).
    *   The *row* of the new pixel (`R_output`) is calculated based on the source row (`R_source`) and the horizontal distance (`dist`) between the framing pixel (`c_frame`) and the closest pixel of the central color segment in that same row. The formula appears to be `R_output = R_source - dist - 1`.
5.  **Row Identification:** The relevant pattern row (`R_source`) seems to be the lowest row in the grid containing at least two different non-background colors adjacent horizontally, forming the structure described in point 2.
6.  **Overwriting:** The added pixels appear in locations that were previously background (white, color 0) in all examples.

**Facts**


```yaml
task_description: Add pixels above a specific horizontal pattern based on distances within the pattern.

element_definitions:
  - name: source_pattern_row
    description: The lowest row in the input grid containing a horizontal sequence like F...F C...C F...F, where F and C are distinct non-background colors.
    properties:
      - row_index (R_source)
      - central_color (C_central)
      - framing_color (F_frame)
      - central_segment_coords: List of (R_source, column) for pixels of C_central.
      - framing_pixel_coords: List of (R_source, column) for pixels of F_frame.

  - name: framing_pixel
    description: An individual pixel of framing_color F_frame within the source_pattern_row.
    properties:
      - coordinate: (R_source, c_frame)
      - color: F_frame

  - name: central_pixel
    description: An individual pixel of central_color C_central within the source_pattern_row.
    properties:
      - coordinate: (R_source, c_central)
      - color: C_central

  - name: added_pixel
    description: A new pixel added to the output grid.
    properties:
      - coordinate: (R_output, c_frame)
      - color: C_central

transformations:
  - action: identify_source_row
    description: Find the lowest row R_source containing the F...F C...C F...F pattern. Determine C_central, F_frame, central_segment_coords, and framing_pixel_coords.
    inputs:
      - input_grid
    outputs:
      - source_pattern_row_details (R_source, C_central, F_frame, central_segment_coords, framing_pixel_coords)

  - action: calculate_added_pixels
    description: For each framing_pixel, calculate the position and color of the corresponding added_pixel.
    inputs:
      - source_pattern_row_details
    outputs:
      - list_of_added_pixels (coordinates and color)
    logic: |
      For each framing_pixel at (R_source, c_frame):
        1. Calculate dist = min(|c_frame - c_central|) for all c_central in central_segment_coords.
        2. Calculate R_output = R_source - dist - 1.
        3. If R_output >= 0, create an added_pixel with coordinate (R_output, c_frame) and color C_central.

  - action: construct_output_grid
    description: Create the output grid by copying the input grid and placing the added_pixels.
    inputs:
      - input_grid
      - list_of_added_pixels
    outputs:
      - output_grid
    logic: |
      1. Copy input_grid to output_grid.
      2. For each added_pixel(coordinate, color):
         Set output_grid[coordinate] = color.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid rows from bottom to top to find the first row (`R_source`) containing at least one contiguous horizontal segment of a non-background color (`C_central`) directly adjacent (horizontally) to pixels of a different non-background color (`F_frame`) on both its left and right sides within that same row.
3.  Identify the column indices of all pixels with color `C_central` in row `R_source` (the `central_segment_columns`).
4.  Identify the coordinates `(R_source, c_frame)` of all pixels with color `F_frame` in row `R_source` (the `framing_pixels`).
5.  For each `framing_pixel` coordinate `(R_source, c_frame)`:
    a.  Calculate the minimum horizontal distance `dist` between `c_frame` and any column index in `central_segment_columns`. (`dist = min(|c_frame - c_central|)`).
    b.  Calculate the target row index `R_output = R_source - dist - 1`.
    c.  If `R_output` is a valid row index (i.e., `R_output >= 0`), set the color of the pixel at `(R_output, c_frame)` in the output grid to `C_central`.
6.  Return the final output grid.
