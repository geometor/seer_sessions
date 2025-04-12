
## train_1

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
4 4 4 4 4 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 4 0
```


**output:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
```


## train_3

**input:**
```
0 0 4 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 4 4 4 4 4
0 0 0 0 0 0
```

## Perception

The input grid is always 6x6 and contains exactly one non-white pixel, which is always yellow (color 4). The background is white (color 0).
The output grid is also 6x6. The transformation rule depends on the column position of the single yellow pixel in the input grid.

1.  **Identify the trigger pixel:** Locate the single non-white (yellow) pixel in the input grid. Note its color and position (row index, column index).
2.  **Determine the fill direction:**
    *   If the yellow pixel is in the first column (column index 0), the transformation fills the entire *row* where the pixel was found with the pixel's color (yellow).
    *   If the yellow pixel is *not* in the first column (column index > 0), the transformation fills the entire *column* where the pixel was found with the pixel's color (yellow).
3.  **Construct the output:** Create an output grid of the same dimensions as the input, initially filled with the background color (white). Then, perform the fill operation (row or column) determined in the previous step using the color of the trigger pixel.

## YAML Facts


```yaml
task_context:
  grid_size:
    fixed: true
    height: 6
    width: 6
  background_color: 0 # white
  input_characteristics:
    - object_count: 1
    - object_type: single_pixel
    - object_color: 4 # yellow
    - unique_pixels: [0, 4] # white, yellow
  output_characteristics:
    - shape: line # can be horizontal or vertical
    - line_color: 4 # yellow
    - background_color: 0 # white
    - unique_pixels: [0, 4] # white, yellow

transformation_logic:
  trigger:
    - find_pixel_by_color:
        color: 4 # yellow
        count: 1
  conditional_rule:
    - condition: pixel_position
      check: column_index
      value: 0
      action_if_true: fill_row_with_color
      action_if_false: fill_column_with_color
  parameters:
    - fill_color: color_of_trigger_pixel
    - fill_target_index:
        if_true: row_index_of_trigger_pixel
        if_false: column_index_of_trigger_pixel

relationship_between_input_output:
  - preservation:
      - grid_dimensions
      - background_color
      - trigger_pixel_color (used for filling)
  - dependency:
      - output_pattern: determined by the column index of the input trigger pixel
      - filled_line_location: determined by the row or column index of the input trigger pixel
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Scan the input grid to find the location (row `r`, column `c`) and color `clr` of the single non-white pixel.
3.  Check if the column index `c` of the found pixel is equal to 0.
4.  If `c` is 0, fill the entire row `r` of the output grid with the color `clr`.
5.  If `c` is not 0, fill the entire column `c` of the output grid with the color `clr`.
6.  Return the modified output grid.
