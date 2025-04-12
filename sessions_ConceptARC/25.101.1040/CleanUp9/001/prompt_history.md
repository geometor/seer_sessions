
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

## Perception

The task involves transforming an input grid into an output grid of the same dimensions.
The input grids contain multiple colors (pixels with values 1-9) on a white background (pixels with value 0).
The output grids consist primarily of a white background and a hollow rectangular frame made of a single color. This color appears to be derived from the input grid.

Specifically:
1.  **Identify Key Color:** The color used for the frame in the output corresponds to the most frequent non-white color in the input grid.
2.  **Determine Initial Frame:** The initial location and size of the frame seem related to the bounding box of all pixels of the key color in the input grid.
3.  **Frame Adjustment:** In the second example, the bounding box of the key color extends further down than the final frame in the output. This suggests an adjustment rule. The bottom edge of the initial bounding box contains only one pixel of the key color. It appears that if any edge (top, bottom, left, right) of the bounding box contains exactly one pixel of the key color, that edge is 'shrunk' inwards. This process might need iteration if shrinking one edge causes another edge to now have only one key color pixel.
4.  **Construct Output:** The final output grid is created by drawing the adjusted hollow rectangular frame using the key color on a white background. All pixels inside and outside the frame are white.

## Facts


```yaml
task_type: transformation
grid_properties:
  dimensionality: 2
  value_range: 0-9
  background_color: 0 # white

input_elements:
  - type: grid
    description: Contains pixels of various colors (1-9) on a white background (0).
  - type: object_set
    description: Implicit objects formed by contiguous pixels of the same non-white color.
  - type: color_frequency
    description: Each non-white color appears a certain number of times.

output_elements:
  - type: grid
    description: Contains a hollow rectangular frame of a single color on a white background.
  - type: object
    name: frame
    description: A hollow rectangle defined by a top-left and bottom-right corner.
    properties:
      color: The single color used for the frame.
      border_pixels: Pixels forming the perimeter of the rectangle.
      interior_pixels: Pixels inside the frame (all white).
      exterior_pixels: Pixels outside the frame (all white).

transformation_steps:
  - step: 1
    action: identify_key_color
    input: input_grid
    output: key_color
    rule: Find the non-white color (1-9) with the highest frequency. If there's a tie, select the color with the lowest numerical value.
  - step: 2
    action: find_key_pixels
    input: input_grid, key_color
    output: key_pixel_locations
    rule: Identify the coordinates of all pixels in the input grid that have the key_color.
  - step: 3
    action: calculate_initial_bounding_box
    input: key_pixel_locations
    output: initial_bbox (min_row, min_col, max_row, max_col)
    rule: Determine the smallest rectangle enclosing all key_pixel_locations.
  - step: 4
    action: adjust_bounding_box
    input: initial_bbox, key_pixel_locations
    output: final_bbox (final_min_row, final_min_col, final_max_row, final_max_col)
    rule: Iteratively check the count of key_color pixels on each of the four borders (top, bottom, left, right) of the current bounding box. If a border contains exactly one key_color pixel, shrink the box by moving that border inwards by one step. Repeat this check until no border shrinks in a full iteration.
  - step: 5
    action: create_output_grid
    input: final_bbox, key_color, input_grid_dimensions
    output: output_grid
    rule: Create a new grid of the same dimensions as the input, filled with the background color (white, 0). Draw the hollow rectangular frame defined by final_bbox using the key_color.

relationships:
  - The output frame's color is determined by the most frequent non-white color in the input.
  - The output frame's position and size are derived from the bounding box of the key color pixels in the input, potentially adjusted by removing edges with only one key color pixel.
```


## Natural Language Program

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Count the occurrences of each non-white color (1 through 9) in the input grid.
3.  Identify the `key_color` which is the non-white color with the highest frequency. If there is a tie in frequency, select the color with the smallest numerical value as the `key_color`.
4.  Find all coordinates `(r, c)` in the input grid where the pixel value equals the `key_color`. Store these as `key_pixel_locations`.
5.  If no pixels of the `key_color` exist, the output is an all-white grid of size HxW; stop.
6.  Calculate the initial bounding box of the `key_pixel_locations`: find the minimum row (`min_r`), minimum column (`min_c`), maximum row (`max_r`), and maximum column (`max_c`).
7.  Initialize the final bounding box coordinates (`final_min_r`, `final_min_c`, `final_max_r`, `final_max_c`) with the initial bounding box values.
8.  Start an adjustment loop:
    a.  Set a flag `shrunk_this_iteration` to false.
    b.  Count how many `key_pixel_locations` lie on the current top border (row = `final_min_r`, column from `final_min_c` to `final_max_c`). If the count is exactly 1 and `final_min_r < final_max_r`, increment `final_min_r` by 1 and set `shrunk_this_iteration` to true.
    c.  Count how many `key_pixel_locations` lie on the current bottom border (row = `final_max_r`, column from `final_min_c` to `final_max_c`). If the count is exactly 1 and `final_max_r > final_min_r`, decrement `final_max_r` by 1 and set `shrunk_this_iteration` to true.
    d.  Count how many `key_pixel_locations` lie on the current left border (column = `final_min_c`, row from `final_min_r` to `final_max_r`). If the count is exactly 1 and `final_min_c < final_max_c`, increment `final_min_c` by 1 and set `shrunk_this_iteration` to true.
    e.  Count how many `key_pixel_locations` lie on the current right border (column = `final_max_c`, row from `final_min_r` to `final_max_r`). If the count is exactly 1 and `final_max_c > final_min_c`, decrement `final_max_c` by 1 and set `shrunk_this_iteration` to true.
    f.  If `shrunk_this_iteration` is true, repeat the adjustment loop (step 8). Otherwise, exit the loop.
9.  Create a new output grid of size HxW, filled entirely with white pixels (value 0).
10. Iterate through all rows `r` from `final_min_r` to `final_max_r`.
11. Iterate through all columns `c` from `final_min_c` to `final_max_c`.
12. If the current coordinate `(r, c)` is on the border of the final bounding box (i.e., if `r == final_min_r` or `r == final_max_r` or `c == final_min_c` or `c == final_max_c`), set the value of the output grid at `(r, c)` to the `key_color`.
13. Return the generated output grid.
