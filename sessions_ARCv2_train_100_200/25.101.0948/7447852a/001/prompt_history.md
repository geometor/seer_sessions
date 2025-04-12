
## train_1

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2
```


## train_2

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

## Perception
The input grids consist of white (0) and red (2) pixels. The output grids are the same size and retain the original red pixels but replace some white pixels with yellow (4) pixels. The transformation appears to operate independently on each row. The placement of yellow pixels depends on the row index and the positions of the red pixels within that row.

Specifically, yellow pixels fill certain segments of white pixels. These segments are defined either by the grid edges and the nearest red pixel, or by pairs of consecutive red pixels within the row. The rule for which segments are filled depends on the row index (0, 1, or 2) and the length of the segment (distance between the red pixels or between a red pixel and the edge).

## Facts


```yaml
task_context:
  description: Fill segments of white pixels with yellow based on row index and proximity to red pixels.
  grid_properties:
    - dimensions: Input and output grids have the same dimensions for each example.
    - colors_used: Input uses white(0) and red(2). Output uses white(0), red(2), and yellow(4).
    - transformation_scope: Row-based; each row is processed independently.

objects:
  - object_type: pixel
    properties:
      - color: white(0), red(2), yellow(4)
      - location: (row, column)
  - object_type: segment
    definition: A contiguous horizontal sequence of white pixels within a row.
    types:
      - left_edge: Starts at column 0, ends before the first red pixel.
      - right_edge: Starts after the last red pixel, ends at the last column.
      - internal: Located between two consecutive red pixels.
    properties:
      - length: Number of pixels in the segment.
      - defining_interval_length: Distance between the red pixels defining the segment (for internal) or distance between the edge and the nearest red pixel (for edge segments).

relationships:
  - relationship_type: adjacency
    description: Red pixels define the boundaries of white pixel segments within each row.
  - relationship_type: conditional_filling
    description: >
      White pixel segments are filled with yellow based on conditions involving the row index and the defining_interval_length of the segment.

actions:
  - action_type: identify_red_pixels
    description: For each row, find the column indices of all red pixels.
  - action_type: identify_segments
    description: Based on red pixel locations and grid edges, identify left_edge, right_edge, and internal white pixel segments for each row.
  - action_type: calculate_interval_lengths
    description: Determine the defining interval length for each segment.
  - action_type: fill_segment
    input: segment, row_index, interval_length
    output: modified_grid (segment pixels changed to yellow)
    conditions:
      - If row index is 0:
        - Fill right_edge segment if its defining_interval_length is 1.
        - Fill internal segment if its defining_interval_length is 4.
      - If row index is 1:
        - Fill left_edge segment if its defining_interval_length is 1.
        - Fill internal segment if its defining_interval_length is 2.
      - If row index is 2:
        - Fill left_edge segment if its defining_interval_length is 2.
        - Fill internal segment if its defining_interval_length is 4.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  For each row `r` in the grid (from top row 0 to bottom row H-1):
    a.  Find the column indices of all red (2) pixels in row `r`. Let this list be `red_cols`.
    b.  Get the width `W` of the grid.
    c.  If `red_cols` is not empty:
        i.  **Check Left Edge Segment:** Let `c_first` be the index of the first red pixel (`red_cols[0]`). If `c_first > 0` (meaning the row starts with white pixels):
            *   Calculate the distance `d_left = c_first`.
            *   If row `r` is 1 and `d_left` is 1, change pixels from column 0 to `c_first - 1` to yellow (4).
            *   If row `r` is 2 and `d_left` is 2, change pixels from column 0 to `c_first - 1` to yellow (4).
        ii. **Check Right Edge Segment:** Let `c_last` be the index of the last red pixel (`red_cols[-1]`). If `c_last < W - 1` (meaning the row ends with white pixels):
            *   Calculate the distance `d_right = (W - 1) - c_last`.
            *   If row `r` is 0 and `d_right` is 1, change pixels from column `c_last + 1` to `W - 1` to yellow (4).
        iii. **Check Internal Segments:** Iterate through pairs of consecutive red pixel indices (`c1`, `c2`) from `red_cols`.
            *   Calculate the interval length `L = c2 - c1`.
            *   If row `r` is 0 or 2, and `L` is 4, change pixels from column `c1 + 1` to `c2 - 1` to yellow (4).
            *   If row `r` is 1, and `L` is 2, change pixels from column `c1 + 1` to `c2 - 1` (which is just column `c1 + 1`) to yellow (4).
3.  Return the modified output grid.
