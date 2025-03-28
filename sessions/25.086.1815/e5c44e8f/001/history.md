
## train_1

**input:**
```
0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 0 0 2 0 0 0
0 0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 0 3 2
0 2 0 3 0 3 3 3 2 3 0
0 3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 0 0 3 0 3 0
0 3 0 3 3 3 3 3 0 3 0
0 3 2 0 0 0 0 0 0 3 2
2 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 0 3 3 3 3 3 3 3 0
0 3 0 3 0 0 0 0 0 3 0
0 3 0 3 0 3 3 3 0 3 0
0 3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 3 0 3 0 3 0
0 3 0 3 0 0 0 3 0 3 0
0 3 0 3 3 3 3 3 0 3 0
0 3 0 0 0 0 0 0 0 3 0
0 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 2 0 0 0 2
0 2 3 0 0 0 0 0 0 0 0
0 0 3 0 3 3 3 0 0 0 0
0 0 3 0 3 0 3 0 0 0 0
0 0 3 0 3 0 3 0 0 2 0
0 2 3 0 0 0 3 0 0 0 0
0 0 3 3 3 3 3 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0 0 0 0
```

Okay, let's analyze the provided examples for this task.

**Perception**

1.  **Grid Size:** All examples use 11x11 grids.
2.  **Colors:** The primary colors involved are White (0), Red (2), and Green (3).
3.  **Input Structure:** Each input grid contains exactly one Green pixel and zero or more Red pixels scattered across a White background.
4.  **Output Structure:** The output grid retains the positions of the original Red and Green pixels from the input. Additionally, some White pixels from the input are changed to Green in the output.
5.  **Core Transformation:** The transformation appears to depend on the presence or absence of Red pixels.
    *   **With Red Pixels (Train 1, Train 3):** The Green color seems to "spread" or "fill" outwards from the initial Green pixel's location. This spread is contained or blocked by the Red pixels, which act like walls. The spread also stops at the grid boundaries. The fill occurs in 4 directions (up, down, left, right).
    *   **Without Red Pixels (Train 2):** When no Red pixels are present in the input, a distinct, seemingly fixed pattern of Green pixels is generated in the output, largely independent of the initial Green pixel's location (except that the initial Green pixel's position is preserved). This pattern involves filling specific rows and columns: alternating columns (1, 3, 5, 7, 9) up to row 8, alternating rows (0, 2, 4, 6, 8) between columns 1 and 9, and the entire last row (row 10).

**Facts**


```yaml
grid_dimensions:
  - height: 11
  - width: 11

pixels:
  - color: 0 (white) # background
  - color: 2 (red)   # barrier/static element
  - color: 3 (green) # source/fill element

input_composition:
  - object: green_pixel
    count: 1
    properties: [source_of_action]
  - object: red_pixels
    count: variable (0 to many)
    properties: [barrier, static]
  - object: white_pixels
    count: variable
    properties: [background, potentially_transformable]

transformation_logic:
  - type: conditional
    condition: presence of red_pixels
    if_present:
      action: flood_fill
      parameters:
        start_point: location of the input green_pixel
        fill_color: 3 (green)
        target_color: 0 (white)
        barriers: locations of red_pixels, grid_boundaries
        connectivity: 4-directional (von Neumann neighborhood)
      effect: changes reachable white_pixels to green_pixels
    if_absent:
      action: generate_pattern
      parameters:
        pattern_definition:
          - type: column_fill
            columns: [1, 3, 5, 7, 9]
            row_range: [0, 8]
            fill_color: 3 (green)
          - type: row_fill
            rows: [0, 2, 4, 6, 8]
            column_range: [1, 9]
            fill_color: 3 (green)
          - type: row_fill
            rows: [10] # last row
            column_range: [0, 10] # full width
            fill_color: 3 (green)
        target_color: 0 (white) # only fill white pixels with the pattern
      effect: changes specific white_pixels to green_pixels based on the fixed pattern

preserved_elements:
  - object: red_pixels
    property: position and color remain unchanged
  - object: initial green_pixel
    property: position and color remain unchanged
```


**Natural Language Program**

1.  Initialize the `output_grid` as an identical copy of the `input_grid`.
2.  Locate the coordinates `(start_row, start_col)` of the single Green (3) pixel in the `input_grid`.
3.  Identify the set of coordinates `barrier_coords` for all Red (2) pixels in the `input_grid`.
4.  **Check if `barrier_coords` is empty:**
    *   **If `barrier_coords` is NOT empty (Red pixels exist):**
        a.  Create a queue and add `(start_row, start_col)` to it.
        b.  Create a set `visited_coords` and add `(start_row, start_col)` to it.
        c.  While the queue is not empty:
            i.  Remove a coordinate `(r, c)` from the front of the queue.
            ii. Examine the four adjacent neighbors `(nr, nc)` (up, down, left, right).
            iii. For each neighbor `(nr, nc)`:
                1. If `(nr, nc)` is within the grid boundaries, AND
                2. If `(nr, nc)` is not in `visited_coords`, AND
                3. If `(nr, nc)` is not in `barrier_coords`, AND
                4. If the pixel at `input_grid[nr][nc]` is White (0):
                    - Add `(nr, nc)` to `visited_coords`.
                    - Add `(nr, nc)` to the queue.
                    - Set `output_grid[nr][nc]` to Green (3).
    *   **If `barrier_coords` IS empty (NO Red pixels exist):**
        a.  Iterate through each cell `(r, c)` of the grid (e.g., row by row, column by column).
        b.  Determine if the cell `(r, c)` matches the fixed pattern criteria:
            - Criterion 1: `0 <= r <= 8` AND `c` is one of {1, 3, 5, 7, 9}.
            - Criterion 2: `r` is one of {0, 2, 4, 6, 8} AND `1 <= c <= 9`.
            - Criterion 3: `r == 10`.
        c.  If the pixel at `output_grid[r][c]` is currently White (0) AND (Criterion 1 OR Criterion 2 OR Criterion 3 is true):
            - Set `output_grid[r][c]` to Green (3).
        d.  (The original Green pixel at `(start_row, start_col)` remains Green because it was copied initially and is not White).
5.  Return the `output_grid`.
