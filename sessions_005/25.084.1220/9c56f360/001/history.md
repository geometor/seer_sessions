
## train_1

**input:**
```
0 0 0 8 0 0 8 3
0 8 0 0 8 0 0 3
8 8 0 8 0 0 8 3
8 8 0 0 0 0 0 3
0 0 0 8 8 0 0 8
8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
```


**output:**
```
0 0 0 8 0 0 8 3
0 8 0 0 8 3 0 0
8 8 0 8 0 0 8 3
8 8 3 0 0 0 0 0
0 0 0 8 8 0 0 8
8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 8 0 0
0 0 8 0 0 8
8 0 0 0 0 8
0 0 8 0 8 0
0 0 0 0 3 3
8 0 8 0 3 3
0 8 0 8 8 0
```


**output:**
```
0 0 0 8 0 0
0 0 8 0 0 8
8 0 0 0 0 8
0 0 8 0 8 0
3 3 0 0 0 0
8 0 8 3 3 0
0 8 0 8 8 0
```


## train_3

**input:**
```
0 0 0 0 8 8 8 8
0 0 0 8 0 8 3 3
8 0 0 8 0 0 3 3
8 8 0 0 0 0 3 3
8 8 0 0 8 8 0 8
0 0 0 8 0 8 0 3
0 8 0 0 0 0 0 3
0 0 0 8 8 0 8 3
8 0 0 8 8 8 0 8
```


**output:**
```
0 0 0 0 8 8 8 8
0 0 0 8 0 8 3 3
8 0 0 8 3 3 0 0
8 8 3 3 0 0 0 0
8 8 0 0 8 8 0 8
0 0 0 8 0 8 3 0
0 8 3 0 0 0 0 0
0 0 0 8 8 0 8 3
8 0 0 8 8 8 0 8
```

Okay, let's analyze the task examples.

## Perception

1.  **Grid Structure:** The input and output are 2D grids of pixels with varying dimensions. The dimensions remain the same between input and output for each example.
2.  **Colors:** The significant colors are white (0), azure (8), and green (3). White appears to be the background. Azure forms static structures. Green pixels are the ones that change position.
3.  **Static Elements:** The azure (8) pixels form patterns that do not change between the input and output grids. They act as obstacles.
4.  **Dynamic Elements:** The green (3) pixels change their positions. Their original locations become white (0) in the output, unless their position doesn't change.
5.  **Movement Pattern:** The green pixels move horizontally within their respective rows, always towards the left (decreasing column index).
6.  **Movement Termination:** A green pixel's leftward movement stops just before it would hit an azure (8) pixel in the same row, or just before it would move off the left edge of the grid. Specifically, it lands in the leftmost white (0) or original green (3) cell available before an azure (8) barrier or the grid edge.
7.  **Collision/Stacking:** If multiple green pixels in the same row are destined for the same landing column (because they are blocked by the same obstacle or the edge), they "stack up" horizontally. The green pixel that was originally furthest to the left lands in the primary target column, the next green pixel lands in the column immediately to its right, and so on. The relative left-to-right order of the green pixels within a row is preserved in their final stacked positions.

## Facts


```yaml
grid_properties:
  - background_color: 0 (white)
  - dimensions_constant: true

objects:
  - id: obstacle
    color: 8 (azure)
    attributes: [static]
    description: Forms fixed horizontal barriers within rows.
  - id: mover
    color: 3 (green)
    attributes: [dynamic]
    description: Represents objects that move horizontally leftwards.

rules:
  - rule_id: movement
    description: >
      Each 'mover' (green pixel) shifts left within its row.
    conditions:
      - The path to the left must not contain an 'obstacle' (azure pixel).
      - Movement stops at the column immediately to the right of the first encountered 'obstacle' or the column 0 if no obstacle is met.
    action: >
      The 'mover' pixel relocates to the determined destination column in the same row.
      The original location of the 'mover' becomes 'background' (white), unless the destination is the same as the origin.
  - rule_id: stacking
    description: >
      Handles collisions where multiple 'movers' in the same row target the same destination column.
    conditions:
      - Multiple 'movers' in row 'r' calculate the same initial target column 'c_target'.
    action: >
      The 'movers' occupy consecutive columns starting from 'c_target', moving rightwards (c_target, c_target + 1, ...).
      The assignment preserves the original relative horizontal order: the leftmost original 'mover' takes the leftmost final position ('c_target').

unchanged_elements:
  - 'obstacle' pixels (azure 8)
  - 'background' pixels (white 0) that are not replaced by moving 'movers' and were not original locations of 'movers'.
```


## Natural Language Program

1.  Initialize an output grid by making a copy of the input grid.
2.  Identify all coordinates `(r, c_orig)` containing green (3) pixels in the input grid.
3.  Temporarily change the color of all identified green pixels in the *output* grid to white (0). This clears their original positions before calculating destinations.
4.  Create a list to store the planned moves, where each entry contains the original coordinates `(r, c_orig)` and the calculated initial target destination coordinate `(r, c_target)`.
5.  For each original green pixel at `(r, c_orig)`:
    a.  Scan leftwards from column `c = c_orig - 1` down to `c = 0` in the *input* grid's row `r`.
    b.  Find the column `c_stop` of the first azure (8) pixel encountered during the scan. If no azure pixel is found, set `c_stop = -1`.
    c.  Calculate the initial target destination column as `c_target = c_stop + 1`.
    d.  Add the tuple `((r, c_orig), (r, c_target))` to the planned moves list.
6.  Process the planned moves to determine final destinations, resolving potential stacking:
    a.  Group the planned moves by their target coordinates `(r, c_target)`.
    b.  For each group targeting the same `(r, c_target)`:
        i.  Retrieve the original coordinates `(r, c_orig)` associated with this target.
        ii. Sort these original coordinates based on their column `c_orig` (ascending).
        iii. Assign final destination columns `c_dest` starting from `c_target` and incrementing by 1 for each subsequent original coordinate in the sorted list (e.g., the first lands at `c_target`, the second at `c_target + 1`, etc.).
        iv. Record the final mapping from `(r, c_orig)` to `(r, c_dest)`.
7.  Update the output grid: For each determined final destination coordinate `(r, c_dest)`, set the pixel `output[r][c_dest]` to green (3).
8.  Return the modified output grid.
