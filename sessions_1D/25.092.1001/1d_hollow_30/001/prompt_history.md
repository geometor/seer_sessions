
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
```


## train_3

**input:**
```
0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0
```

**Perception of Task Elements:**

The task operates on single-row grids (1D arrays). Each input grid contains a single contiguous horizontal segment of a non-white color, surrounded by white pixels. The transformation isolates the endpoints of this non-white segment. The color of the segment is preserved at these endpoints, while the interior pixels of the segment are changed to white. Pixels outside the original segment remain unchanged (white).

**YAML Facts:**


```yaml
task_type: object_transformation
dimensionality: 1D # Grids are effectively 1-dimensional arrays
objects:
  - type: segment
    attributes:
      color: non-white (variable, e.g., blue, red, orange)
      contiguity: horizontal
      count_per_input: 1
    relationships:
      location: surrounded by white pixels
actions:
  - name: identify_segment
    input: input_grid
    output: segment_properties (color, start_index, end_index)
  - name: create_output_grid
    based_on: input_grid_dimensions
    initial_state: all_white_pixels
  - name: preserve_endpoints
    target: output_grid
    using: segment_properties
    effect: set pixels at start_index and end_index to the segment's color
relationships_transformation:
  - input_segment_interior_pixels -> output_white_pixels
  - input_segment_endpoint_pixels -> output_endpoint_pixels (color preserved)
  - input_surrounding_white_pixels -> output_surrounding_white_pixels (unchanged)
invariance:
  - grid_dimensions
  - color_of_endpoints
  - position_of_endpoints
  - surrounding_white_pixels
variance:
  - color_of_non_white_segment (between examples)
  - length_of_non_white_segment
  - position_of_non_white_segment
  - interior_pixels_of_segment (change from non-white to white)
```


**Natural Language Program:**

1.  Receive the input grid (a single row of pixels).
2.  Scan the grid to locate the contiguous horizontal segment of non-white pixels.
3.  Record the color of this segment, its starting column index, and its ending column index.
4.  Create a new grid with the same dimensions as the input grid, filled entirely with white pixels (0).
5.  In the new grid, set the pixel at the recorded starting column index to the recorded segment color.
6.  In the new grid, set the pixel at the recorded ending column index to the recorded segment color.
7.  Output the modified grid.
