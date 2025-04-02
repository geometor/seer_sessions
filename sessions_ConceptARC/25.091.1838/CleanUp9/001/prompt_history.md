
## train_1

**input:**
```
0 4 0 0 2 3
4 1 1 2 1 0
0 1 0 0 2 3
0 2 0 0 1 0
0 2 1 1 1 0
0 2 0 0 4 0
```


**output:**
```
0 0 0 0 0 0
0 1 1 1 1 0
0 1 0 0 1 0
0 1 0 0 1 0
0 1 1 1 1 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 6 5 6
0 5 0 0 0 6
0 3 0 0 0 5
0 3 0 3 0 5
0 5 5 5 5 5
6 6 0 5 0 3
```


**output:**
```
0 5 5 5 5 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 0 0 0 5
0 5 5 5 5 5
0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Input/Output Grid Size:** Both input and output grids in the examples maintain the same dimensions (6x6).
2.  **Color Palette:** The input grids use multiple colors (white, yellow, blue, red, green in train_1; white, gray, magenta, green in train_2). The output grids use only two colors: white (0) as the background and one other color (blue (1) in train_1, gray (5) in train_2).
3.  **Dominant Color:** In each input grid, there appears to be one non-white color that is more frequent than others (blue in train_1, gray in train_2). Let's call this the "frame color".
4.  **Transformation:** The core transformation seems to involve identifying the spatial extent (bounding box) of the frame color pixels in the input.
5.  **Output Structure:** The output consists of a hollow rectangle drawn using the frame color, positioned according to the bounding box derived from the input. The interior of the rectangle and the area outside the rectangle are filled with the background color (white).
6.  **Other Colors:** All input colors other than the identified frame color and the background color are discarded or overwritten in the output.

## Facts


```yaml
task_type: object_transformation # Could also be considered pattern generation based on input features

components:
  - role: input_grid
    attributes:
      - grid_dimensions: variable (e.g., 6x6 in examples)
      - background_color: white (0)
      - foreground_colors: multiple, variable
      - key_feature: distribution of pixels for one specific non-background color (frame_color)

  - role: output_grid
    attributes:
      - grid_dimensions: same as input_grid
      - background_color: white (0)
      - foreground_colors: single color (frame_color from input)
      - structure: hollow rectangle defined by the frame_color

actions:
  - identify_frame_color:
      description: Determine the non-background color with the highest pixel count in the input grid.
      input: input_grid
      output: frame_color (e.g., blue(1) or gray(5))
  - calculate_bounding_box:
      description: Find the minimum and maximum row and column indices containing any pixel of the frame_color.
      input: input_grid, frame_color
      output: bounding_box {min_row, max_row, min_col, max_col}
  - generate_output_grid:
      description: Create a new grid of the same dimensions as the input, filled with the background color.
      input: input_grid_dimensions
      output: initial_output_grid
  - draw_hollow_rectangle:
      description: Set the pixels along the perimeter defined by the bounding_box to the frame_color on the output grid.
      input: initial_output_grid, bounding_box, frame_color
      output: final_output_grid

relationships:
  - The frame_color in the output is determined by the most frequent non-background color in the input.
  - The position and size of the hollow rectangle in the output are determined by the bounding box of the frame_color pixels in the input.
  - All pixels in the output grid are either the background color (white) or the frame_color.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid's dimensions, filled entirely with the background color (white, 0).
2.  Analyze the input grid to find the non-background color (any color other than white, 0) that appears most frequently. Designate this color as the `frame_color`.
3.  Identify all pixels in the input grid that have the `frame_color`.
4.  Determine the bounding box enclosing all `frame_color` pixels found in step 3. This involves finding the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among these pixels.
5.  Modify the output grid: For all pixels lying on the perimeter of the bounding box calculated in step 4, change their color to the `frame_color`. Specifically:
    *   Set pixels at `(min_row, c)` to `frame_color` for `c` from `min_col` to `max_col`.
    *   Set pixels at `(max_row, c)` to `frame_color` for `c` from `min_col` to `max_col`.
    *   Set pixels at `(r, min_col)` to `frame_color` for `r` from `min_row` to `max_row`.
    *   Set pixels at `(r, max_col)` to `frame_color` for `r` from `min_row` to `max_row`.
6.  Ensure all other pixels in the output grid (those inside the hollow rectangle and those outside the bounding box) remain the background color (white, 0).
7.  Return the modified output grid.
