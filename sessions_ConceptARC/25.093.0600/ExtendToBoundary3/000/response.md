Okay, let's break down the task based on the provided examples.

### Perception

1.  **Grid Structure:** Both input and output are 2D grids of integers. The value `0` represents the background. Non-zero integers represent distinct objects or markers.
2.  **Core Task:** The transformation involves selectively "painting" or "filling" areas of the grid based on the location and value of specific non-zero cells in the input. The original non-zero cells seem to remain unchanged.
3.  **Trigger Locations & Actions:** There appear to be three distinct trigger conditions based on the location of a non-zero cell in the input grid:
    *   **Right Edge:** A non-zero cell in the last column triggers a horizontal fill leftwards in the same row.
    *   **Second-to-Last Row:** A non-zero cell in the second-to-last row triggers a vertical fill upwards in the same column.
    *   **Left Edge:** A non-zero cell in the first column triggers a diagonal fill upwards and rightwards.
4.  **Fill Color:** The fill operation uses the color (integer value) of the trigger cell.
5.  **Stopping Conditions:** The fill operations do not overwrite existing non-zero cells from the input. Each fill type has specific conditions that stop its propagation:
    *   **Horizontal Fill (Leftwards):** Stops upon encountering any non-zero cell in the same row to its left.
    *   **Vertical Fill (Upwards):** Stops upon encountering a non-zero cell in the same column above it, OR stops just before reaching a row that contains *any* non-zero cell.
    *   **Diagonal Fill (Up-Right):** Stops upon encountering any non-zero cell on its diagonal path, OR stops if the current fill position `(nr, nc)` satisfies `nr <= R` and `nc >= C` for any *other* non-zero cell `(R, C)` present in the original input. It also stops if it goes out of the grid boundaries.
6.  **Independence:** Each trigger cell initiates its fill independently based on the *input* grid state. The resulting fills are combined in the output grid.

### Facts


```yaml
Grid:
  Type: 2D Array of Integers
  BackgroundValue: 0
Objects:
  Type: Non-zero integer cells
  Properties:
    - value (color)
    - position (row, column)
Relationships:
  - Relative Position: Cells can be located at edges (first/last column, last-but-one row) or internally.
  - Proximity: For diagonal fills, the position relative to *other* non-zero cells matters.
Actions:
  - Identify Triggers: Locate non-zero cells based on specific positions (last column, second-last row, first column).
  - Fill: Propagate the trigger cell's value into adjacent background cells according to specific rules.
    - Fill Directions:
      - Horizontal Left (from last column)
      - Vertical Up (from second-last row)
      - Diagonal Up-Right (from first column)
    - Fill Stopping Conditions:
      - Boundary Hit (edge of grid)
      - Collision (encountering a non-zero cell from the input grid)
      - Proximity Constraint (specific condition for diagonal fill related to other objects)
      - Row Constraint (specific condition for vertical fill related to non-empty rows above)
Transformation:
  Rule: Apply fill actions originating from all identified trigger cells onto a copy of the input grid.
  InputPreservation: Original non-zero cells from the input are preserved in the output.
  OutputComposition: The final output is the initial grid state modified by all triggered fill operations.
```


### Natural Language Program

1.  **Initialize:** Create the output grid as an exact copy of the input grid.
2.  **Identify Triggers:** Find all cells `(r, c)` in the input grid that have a non-zero value `V`.
3.  **Process Triggers:** For each identified non-zero trigger cell `(r, c)` with value `V`:
    a.  **Right Edge Trigger:** If the cell is in the last column (`c == width - 1`):
        *   Iterate leftwards from `k = c - 1` down to 0.
        *   If the input cell `input[r][k]` is non-zero, stop this fill.
        *   Otherwise, set the output cell `output[r][k] = V`.
    b.  **Second-to-Last Row Trigger:** If the cell is in the second-to-last row (`r == height - 2`):
        *   Iterate upwards from `i = r - 1` down to 0.
        *   Check if the entire input row `i` contains any non-zero value. If yes, stop this fill.
        *   If the input cell `input[i][c]` is non-zero, stop this fill.
        *   Otherwise, set the output cell `output[i][c] = V`.
    c.  **Left Edge Trigger:** If the cell is in the first column (`c == 0`):
        *   Find the locations `(R, C)` of all *other* non-zero cells in the input grid.
        *   Iterate with `j` starting from 1.
        *   Calculate the potential fill coordinates `nr = r - j`, `nc = c + j`.
        *   If `nr` or `nc` are outside the grid boundaries, stop this fill.
        *   If the input cell `input[nr][nc]` is non-zero, stop this fill.
        *   Check the proximity condition: For each other non-zero cell `(R, C)`, if `nr <= R` AND `nc >= C`, stop this fill.
        *   If none of the stopping conditions are met, set the output cell `output[nr][nc] = V`.
4.  **Finalize:** Return the modified output grid.