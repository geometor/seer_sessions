
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
```


## train_2

**input:**
```
3 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

## Perception

1.  **Grid Size:** Both input and output grids in all examples are 10x10.
2.  **Background Color:** The predominant color in both input and output grids is white (0).
3.  **Input Objects:** In the input grids, non-white pixels (Red-2, Green-3, Yellow-4, Azure-8) appear *only* in the first column (index 0). Each non-white pixel seems to be an independent object.
4.  **Output Objects:** In the output grids, the same non-white pixels from the input's first column appear, but they have been moved horizontally to different columns. The original positions in the first column become white.
5.  **Transformation:** The core transformation is the horizontal movement (translation) of each non-white pixel found in the first column. The row of the pixel remains unchanged. The destination column seems to depend solely on the *color* of the pixel.
6.  **Color-Column Mapping:** By comparing the input color in column 0 with its output column position across all examples, we can deduce the following mapping:
    *   Red (2) moves to column index 2.
    *   Azure (8) moves to column index 1.
    *   Green (3) moves to column index 4.
    *   Yellow (4) moves to column index 3.
7.  **Consistency:** This color-to-column mapping rule is consistent across all three training examples. Pixels in rows that start with white (0) in the input remain white in the output, and no new colors are introduced.

## YAML Facts


```yaml
task_context:
  grid_properties:
    size: 10x10
    background_color: 0 # white
  input_elements:
    - element_type: pixel_objects
      location: Column 0
      colors_present: [2, 3, 4, 8] # red, green, yellow, azure
      background: white (0) fills the rest of the grid
  output_elements:
    - element_type: pixel_objects
      location: Columns 1, 2, 3, 4 (variable, depends on input color)
      colors_present: [2, 3, 4, 8] # same as input
      background: white (0) fills the rest of the grid, including the original positions in column 0
transformation:
  action: move_pixel
  affected_elements: non-white pixels in column 0
  movement:
    axis: horizontal
    row_change: none
    column_change_rule: determined by a fixed mapping based on the pixel's color value
  color_to_column_mapping:
    2: 2 # red -> column 2
    3: 4 # green -> column 4
    4: 3 # yellow -> column 3
    8: 1 # azure -> column 1
  output_grid_initialization: Start with an all-white grid of the same size as the input.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with white pixels (color 0).
2.  Iterate through each row of the input grid, from top to bottom (row index `r` from 0 to height-1).
3.  For each row `r`, examine the pixel at column index 0. Let its color value be `c`.
4.  If the color `c` is not white (i.e., `c != 0`):
    a.  Determine the target column index `target_col` based on the color `c` using this specific mapping:
        *   If `c` is 2 (Red), `target_col` is 2.
        *   If `c` is 3 (Green), `target_col` is 4.
        *   If `c` is 4 (Yellow), `target_col` is 3.
        *   If `c` is 8 (Azure), `target_col` is 1.
    b.  Set the pixel in the output grid at row `r` and column `target_col` to the color `c`.
5.  Return the completed output grid.
