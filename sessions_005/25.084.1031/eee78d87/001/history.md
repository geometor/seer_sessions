
## train_1

**input:**
```
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 3 7
7 7 7 3 3 3
7 7 7 7 3 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
7 7 7 7 7 7
7 1 7 1 7 7
7 1 1 1 7 7
7 1 7 1 7 7
7 7 7 7 7 7
7 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
0 0 0 0 0 9 9 9 9 9 9 0 0 0 0 0
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
7 7 7 7 7 7
7 6 7 6 7 7
7 7 6 7 7 7
7 6 7 6 7 7
7 7 7 7 7 7
7 7 7 7 7 7
```


**output:**
```
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
0 7 7 0 7 7 9 7 7 9 7 7 0 7 7 0
7 0 0 7 0 9 7 9 9 7 9 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
7 0 0 7 0 0 7 0 0 7 0 0 7 0 0 7
0 7 7 0 7 7 0 7 7 0 7 7 0 7 7 0
```

Okay, let's break down this ARC task.

## Perception of Task Elements

1.  **Input Grid:** The input is always a 6x6 grid. It predominantly consists of an orange (7) background. In each example, there's a small, contiguous shape made of a different color (green=3, blue=1, or magenta=6). The shape's specific color and exact position vary between examples.
2.  **Output Grid:** The output is always a larger 16x16 grid. It has a structured pattern based on the input.
3.  **Transformation Pattern:**
    *   The output grid size (16x16) relates to the input size (6x6) by the formula `(Input_Dim * 3 - 2)`. (6 * 3 - 2 = 16).
    *   The output grid seems to be constructed by mapping each input pixel to a 3x3 region in the output, with overlaps creating the final structure.
    *   Specifically, each orange (7) pixel in the input corresponds to a 2x2 block of orange `[[7, 7], [7, 7]]` placed in the output grid. The top-left corner of this 2x2 block is at `(row * 3, col * 3)`, where `(row, col)` are the coordinates in the input grid.
    *   The spaces between these 2x2 orange blocks are filled with white (0), creating a grid-like pattern.
    *   Crucially, if the input grid contains *any* pixel that is *not* orange (i.e., if the colored shape is present), a fixed 6x6 block of maroon (9) is placed in the center of the output grid. This maroon block covers rows 5 through 10 and columns 5 through 10 (inclusive), overwriting any orange or white pixels that were previously placed there.
    *   The specific color or position of the non-orange shape in the input does not affect the *content* or *position* of the maroon block in the output; its mere *presence* triggers the maroon block overlay.

## YAML Fact Document


```yaml
task_context:
  description: Transforms a 6x6 input grid into a 16x16 output grid based on pixel color and the presence of a non-background shape.
  input_grid_size: [6, 6]
  output_grid_size: [16, 16]
  output_size_relation: "(Input_Dim * 3) - 2"
  background_color: 7 # orange
  shape_colors: [3, 1, 6] # green, blue, magenta seen in examples
  overlay_color: 9 # maroon
  overlay_trigger: Presence of any non-background color pixel in the input grid.
  overlay_shape: Fixed 6x6 square.
  overlay_position: Fixed at rows 5-10, columns 5-10 (0-indexed).

transformation_steps:
  - step: 1
    action: Initialize output grid
    parameters:
      height: "(Input_Height * 3) - 2"
      width: "(Input_Width * 3) - 2"
      fill_color: 0 # white
  - step: 2
    action: Iterate through input grid pixels
    parameters:
      input_pixel_coords: (r, c)
      input_pixel_value: color
  - step: 3
    condition: color == background_color (7)
    action: Place pattern in output grid
    parameters:
      pattern: [[7, 7], [7, 7]]
      output_top_left_coords: (r * 3, c * 3)
  - step: 4
    action: Check for non-background pixels
    parameters:
      input_grid: entire input grid
      background_color: 7
    result: stores boolean `shape_present`
  - step: 5
    condition: shape_present == True
    action: Place overlay pattern in output grid
    parameters:
      pattern: 6x6 block of overlay_color (9)
      output_top_row: 5
      output_bottom_row: 10
      output_left_col: 5
      output_right_col: 10
      behavior: Overwrite existing pixels

relationship_summary:
  - Each input pixel maps conceptually to a 3x3 area in the output grid.
  - Input background pixels generate a 2x2 orange pattern at the top-left of their mapped area.
  - Input non-background pixels do not directly generate a pattern based on their own color.
  - The existence of *any* non-background pixel triggers a constant maroon overlay in a fixed central position on the output grid.
```


## Natural Language Program

1.  Define the background color as orange (7) and the overlay color as maroon (9).
2.  Read the input grid and determine its height (H) and width (W).
3.  Calculate the output grid dimensions: `output_height = H * 3 - 2`, `output_width = W * 3 - 2`.
4.  Create a new output grid of the calculated dimensions and initialize all its pixels to white (0).
5.  Initialize a flag `shape_detected` to `False`.
6.  Iterate through each pixel of the input grid at coordinates `(r, c)` from `(0, 0)` to `(H-1, W-1)`.
7.  Let `current_color` be the color of the input pixel at `(r, c)`.
8.  If `current_color` is the background color (orange, 7):
    *   Draw a 2x2 block of orange (7) onto the output grid. The top-left pixel of this block should be at `(r * 3, c * 3)`. Specifically, set `output[r*3, c*3]`, `output[r*3+1, c*3]`, `output[r*3, c*3+1]`, and `output[r*3+1, c*3+1]` to 7.
9.  Else (if `current_color` is not the background color):
    *   Set the `shape_detected` flag to `True`.
10. After iterating through all input pixels, check the `shape_detected` flag.
11. If `shape_detected` is `True`:
    *   Draw a 6x6 block of the overlay color (maroon, 9) onto the output grid. This block should cover rows 5 through 10 (inclusive) and columns 5 through 10 (inclusive). This overwrites any colors previously placed in this region.
12. Return the final output grid.
