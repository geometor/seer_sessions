Okay, let's analyze the task examples.

### Perception

1.  **Grid Structure:** The input and output are both 2D grids of pixels with the same dimensions in each example.
2.  **Colors Involved:** The primary colors involved in the transformation are green (3) and azure (8). White (0) acts as the background and replaces the original positions of moved green pixels. Other colors, if present, seem unaffected.
3.  **Core Action:** The transformation involves moving green (3) pixels horizontally within their respective rows.
4.  **Direction of Movement:** Green pixels consistently move towards the left (decreasing column index).
5.  **Stopping Condition:** The movement of a green pixel stops based on the presence of azure (8) pixels in the same row, to its left. Specifically, a green pixel attempts to move to the column immediately to the right of the *first* azure pixel encountered when scanning leftwards from the green pixel's original position.
6.  **Edge Condition:** If there are no azure pixels to the left of a green pixel in its row, it moves to the leftmost column (column 0).
7.  **No Movement Condition:** If a green pixel is already located immediately to the right of the first azure pixel to its left, it does not move.
8.  **Collision/Stacking:** When multiple green pixels in the same row target the same destination column, or adjacent columns that would result in overlap after movement, they "stack" or shift. The green pixel originating from the rightmost column lands in its calculated target column first. Subsequent green pixels (moving from right-to-left processing) targeting an already occupied cell will land in the next available column to the right.
9.  **State Change:** The original position of a green pixel that moves becomes white (0). Pixels that are not green (3) or are not the original positions of moved green pixels remain unchanged.

### Facts


```yaml
task_elements:
  - grid:
      type: 2D array of integers (pixels)
      properties:
        - Variable dimensions (height, width) between examples.
        - Input and output grids have the same dimensions for a given example.
  - pixels:
      types:
        - background: white (0)
        - active: green (3)
        - obstacle: azure (8)
        - static: other colors (remain unchanged)
  - objects:
      - green_pixel:
          color: 3
          behavior: Moves leftward within its row.
      - azure_pixel:
          color: 8
          behavior: Acts as a stationary obstacle influencing green pixel movement.
  - relationships:
      - adjacency: A green pixel's movement stops based on horizontal adjacency to an azure pixel.
      - row_containment: Movement is constrained within the pixel's original row.
      - left_of: The relevant azure obstacle is the first one found to the left of the green pixel.
  - actions:
      - move_left: Performed by green pixels.
      - stop: Green pixel movement halts based on conditions (obstacle, edge, existing position).
      - replace: Original position of a moved green pixel is replaced with white (0).
      - resolve_collision: If multiple green pixels target overlapping destinations, subsequent pixels shift right.
  - constraints:
      - grid_boundary: Left edge (column 0) acts as a boundary if no azure obstacle exists.
      - obstacle_priority: Azure pixels take precedence over the grid edge as stopping points.
      - processing_order: Collisions are resolved based on a right-to-left processing order of green pixels within a row.
```


### Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row `r` of the grid, from top to bottom.
3.  For the current row `r`, find the column indices `c` of all green (3) pixels. Store these indices.
4.  Create a list or map to track the occupied destination cells within the current row `r` for this processing step.
5.  Iterate through the identified green pixel column indices `c` for row `r` in descending order (from right to left).
6.  For each green pixel at original position `(r, c)`:
    a.  Scan leftwards from column `c-1` down to column 0 in row `r`. Find the column index `az_c` of the first (rightmost) azure (8) pixel encountered.
    b.  Determine the target column `target_c`:
        i.  If an azure pixel was found at `az_c`, set `target_c = az_c + 1`.
        ii. If no azure pixel was found to the left, set `target_c = 0`.
    c.  If the green pixel's current column `c` is already equal to `target_c`, this pixel does not move; continue to the next green pixel.
    d.  If `c` is not equal to `target_c`:
        i.  Initialize the final destination column `dest_c = target_c`.
        ii. While the position `(r, dest_c)` has already been marked as an occupied destination in the current row's processing step, increment `dest_c` by 1.
        iii. Mark `(r, dest_c)` as an occupied destination for this row's processing step.
        iv. Update the output grid: Set the pixel at the original position `(r, c)` to white (0).
        v. Update the output grid: Set the pixel at the destination position `(r, dest_c)` to green (3).
7.  After processing all rows, return the modified output grid.