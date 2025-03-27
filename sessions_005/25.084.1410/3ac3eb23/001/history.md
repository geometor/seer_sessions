
## train_1

**input:**
```
0 4 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
```


## train_2

**input:**
```
0 2 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
```

**Perception of Task Elements:**

1.  **Input Grid:** The input is a 2D grid containing mostly white pixels (0) and one or more isolated non-white pixels located somewhere in the grid.
2.  **Output Grid:** The output is a grid of the same dimensions as the input. The original non-white pixels from the input persist in the output. Additionally, new non-white pixels appear below the original ones, forming a branching or cascading pattern downwards.
3.  **Color Preservation:** The color of the cascading pixels matches the color of the original source pixel.
4.  **Cascade Pattern:** For each non-white pixel at `(row, col)`, new pixels of the same color are potentially generated in the row below (`row + 1`) at positions `(row + 1, col - 1)` and `(row + 1, col + 1)`.
5.  **Conditions for Generation:** A new pixel is generated at a target position only if:
    *   The target position is within the grid boundaries.
    *   The target position in the grid is currently white (0). If multiple cascades might write to the same location, the first one to "claim" the white pixel determines its color. (Observation: in the examples, the propagation seems to happen row by row, so conflicts within the same row generation step don't seem possible based on the `(r+1, c-1)` and `(r+1, c+1)` rule).
6.  **Iteration:** The cascading process repeats row by row. Pixels generated in row `r+1` can themselves generate new pixels in row `r+2`, following the same rules.
7.  **Independence:** If there are multiple initial non-white pixels, each one initiates its own cascade independently, using its specific color.

**YAML Facts:**


```yaml
task_description: Propagate colored pixels downwards in a cascading pattern.
grid_properties:
  dimensionality: 2
  value_range: 0-9 (colors)
  background_color: 0 (white)
objects:
  - type: colored_pixel
    attributes:
      - color: (non-zero value)
      - position: (row, column)
    initial_state: Present in the input grid.
relationships:
  - type: propagation
    source: colored_pixel at (r, c) with color X
    target_potential:
      - position: (r+1, c-1)
      - position: (r+1, c+1)
    condition:
      - target position is within grid bounds.
      - target position currently holds the background color (0).
    action: Change the color of the target position to X.
transformation:
  - type: iterative_process
    scope: grid
    steps:
      - Initialize the output grid as a copy of the input grid.
      - Iterate through rows `r` from 0 up to `height - 2`.
      - For each column `c` from 0 up to `width - 1`:
          - Identify the color `X` at `(r, c)` in the current state of the output grid.
          - If `X` is not the background color (0):
              - Apply the propagation relationship to potentially color pixels at `(r+1, c-1)` and `(r+1, c+1)` in the output grid according to the specified conditions.
  - result: The final state of the output grid after all iterations.
```


**Natural Language Program:**

1.  Create a copy of the input grid; this will be the working output grid.
2.  Iterate through each row of the working grid, from the top row (row index 0) down to the second-to-last row (row index `height - 2`). Let the current row index be `r`.
3.  Within each row `r`, iterate through each column (column index `c`) from left to right (index 0 to `width - 1`).
4.  Examine the pixel at position `(r, c)` in the working grid. Let its color be `current_color`.
5.  If `current_color` is not white (0):
    a.  Consider the target position `(r + 1, c - 1)` (down-left).
        i.  Check if this position is within the grid boundaries (row `r+1` is less than grid height, column `c-1` is greater than or equal to 0).
        ii. If it is within bounds, check the color of the pixel at `(r + 1, c - 1)` in the working grid.
        iii.If the color at `(r + 1, c - 1)` is white (0), change its color to `current_color`.
    b.  Consider the target position `(r + 1, c + 1)` (down-right).
        i.  Check if this position is within the grid boundaries (row `r+1` is less than grid height, column `c+1` is less than grid width).
        ii. If it is within bounds, check the color of the pixel at `(r + 1, c + 1)` in the working grid.
        iii.If the color at `(r + 1, c + 1)` is white (0), change its color to `current_color`.
6.  After iterating through all relevant rows and columns, the working grid contains the final output. Return this grid.
