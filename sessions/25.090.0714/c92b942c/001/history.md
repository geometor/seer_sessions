
## train_1

**input:**
```
0 0 0
0 6 0
0 0 0
```


**output:**
```
3 0 0 3 0 0 3 0 0
1 6 1 1 6 1 1 6 1
0 0 3 0 0 3 0 0 3
3 0 0 3 0 0 3 0 0
1 6 1 1 6 1 1 6 1
0 0 3 0 0 3 0 0 3
3 0 0 3 0 0 3 0 0
1 6 1 1 6 1 1 6 1
0 0 3 0 0 3 0 0 3
```


## train_2

**input:**
```
0 0 5 0
0 0 0 0
```


**output:**
```
1 1 5 1 1 1 5 1 1 1 5 1
0 3 0 3 0 3 0 3 0 3 0 3
1 1 5 1 1 1 5 1 1 1 5 1
0 3 0 3 0 3 0 3 0 3 0 3
1 1 5 1 1 1 5 1 1 1 5 1
0 0 0 3 0 3 0 3 0 3 0 3
```


## train_3

**input:**
```
0 0 0 0 0 0
0 0 4 0 0 0
0 0 0 0 0 0
4 0 0 0 4 0
```


**output:**
```
0 3 0 0 0 0 0 3 0 0 0 0 0 3 0 0 0 0
1 1 4 1 1 1 1 1 4 1 1 1 1 1 4 1 1 1
0 0 0 3 0 3 0 0 0 3 0 3 0 0 0 3 0 0
4 1 1 1 4 1 4 1 1 1 4 1 4 1 1 1 4 1
0 3 0 0 0 3 0 3 0 0 0 3 0 3 0 0 0 3
1 1 4 1 1 1 1 1 4 1 1 1 1 1 4 1 1 1
0 0 0 3 0 3 0 0 0 3 0 3 0 0 0 3 0 0
4 1 1 1 4 1 4 1 1 1 4 1 4 1 1 1 4 1
0 3 0 0 0 3 0 3 0 0 0 3 0 3 0 0 0 3
1 1 4 1 1 1 1 1 4 1 1 1 1 1 4 1 1 1
0 0 0 3 0 3 0 0 0 3 0 3 0 0 0 3 0 0
4 1 1 1 4 1 4 1 1 1 4 1 4 1 1 1 4 1
```


## train_4

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 3 0 0 0
1 1 2 1 1 1 1 2 1 1 1 1 2 1 1
0 0 0 3 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 3 0 0 0
1 1 2 1 1 1 1 2 1 1 1 1 2 1 1
0 0 0 3 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 3 0 0 0
1 1 2 1 1 1 1 2 1 1 1 1 2 1 1
0 0 0 3 0 0 0 0 3 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception of Task Elements**

1.  **Input/Output Relationship:** The output grid is always exactly 3 times larger than the input grid in both height and width. This suggests a tiling operation where the input grid (or a modified version of it) is repeated 3x3 times to form the output.
2.  **Color Preservation:** Non-white pixels (colors 1 through 9) present in the input grid seem to retain their original color and relative positions within each tile of the output grid.
3.  **Color Transformation (White Pixels):** White pixels (color 0) in the input grid are transformed into either blue (color 1) or green (color 3) in the output grid.
4.  **Transformation Logic:** The transformation of white pixels depends on their spatial relationship to the non-white pixels in the original input grid.
    *   White pixels that are orthogonally adjacent (sharing a side, not just a corner) to any non-white pixel in the input grid are transformed into blue (1).
    *   White pixels that are *not* orthogonally adjacent to any non-white pixel (including those only diagonally adjacent or further away) are transformed into green (3).
5.  **Process:** The transformation likely involves two main steps:
    *   First, determine the color transformation for each pixel in the input grid based on the adjacency rule described above. This creates a "modified" version of the input grid pattern.
    *   Second, tile this modified pattern 3 times horizontally and 3 times vertically to create the final output grid.

**YAML Facts**


```yaml
task_type: pattern_modification_and_tiling
input_grid:
  properties:
    - contains_pixels_of_various_colors
    - dimensions_vary_per_example
    - contains_at_least_one_non_white_pixel
    - white_pixels_exist_in_relation_to_non_white_pixels (adjacent, non-adjacent)
output_grid:
  properties:
    - dimensions_are_exactly_3_times_input_dimensions (height_out = 3 * height_in, width_out = 3 * width_in)
    - structure_is_a_3x3_tiling_of_a_base_pattern
base_pattern:
  derivation: derived_from_input_grid
  properties:
    - same_dimensions_as_input_grid
    - non_white_pixels_from_input_retain_their_color_and_position
    - white_pixels_from_input_are_recolored
color_transformation_rule:
  applies_to: white_pixels_in_input
  conditions:
    - if_orthogonally_adjacent_to_any_non_white_pixel:
        output_color: blue (1)
    - otherwise:
        output_color: green (3)
tiling_operation:
  type: spatial_repetition
  pattern: base_pattern (modified_input)
  repetitions: 3x3 grid
```


**Natural Language Program**

1.  Identify all non-white pixels in the input grid. Let's call these the "source" pixels.
2.  Create a new grid (the "modified pattern") with the same dimensions as the input grid.
3.  Iterate through each pixel location (row, col) in the input grid:
    a.  If the pixel at (row, col) in the input grid is a source pixel (non-white), copy its color to the same location (row, col) in the modified pattern grid.
    b.  If the pixel at (row, col) in the input grid is white (0):
        i.  Check if this white pixel shares an edge (is orthogonally adjacent) with *any* source pixel in the input grid.
        ii. If it is orthogonally adjacent to at least one source pixel, set the color at (row, col) in the modified pattern grid to blue (1).
        iii. If it is *not* orthogonally adjacent to any source pixel, set the color at (row, col) in the modified pattern grid to green (3).
4.  Create the final output grid, which is 3 times the height and 3 times the width of the input grid.
5.  Fill the output grid by tiling the modified pattern grid 3 times horizontally and 3 times vertically. (The pixel at output[r][c] will have the color of the pixel at modified_pattern[r % height_in][c % width_in]).
