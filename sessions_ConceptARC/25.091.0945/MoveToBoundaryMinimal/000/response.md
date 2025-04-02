**Perception:**

The task involves moving a single, isolated pixel within a grid until it reaches a position adjacent to a boundary line.

1.  **Identify Objects:**
    *   **Background:** Primarily white (0) pixels.
    *   **Mover Pixel:** A single pixel of a specific color (green in example 1, magenta in example 2) that is not part of the boundary.
    *   **Boundary Line:** A contiguous line of pixels (vertical yellow line in example 1, horizontal green line in example 2).
2.  **Identify Transformation:** The 'mover' pixel changes its position; all other pixels remain unchanged.
3.  **Movement Rule:** The 'mover' pixel travels in a straight line (horizontally or vertically) towards the 'boundary' line.
    *   If the boundary is vertical, the movement is horizontal.
    *   If the boundary is horizontal, the movement is vertical.
4.  **Stopping Condition:** The movement stops when the 'mover' pixel reaches the cell immediately adjacent (left/right or above/below) to the boundary line along its path of movement. The mover pixel does not land *on* the boundary line itself.

**Facts:**


```yaml
task_type: object_movement
objects:
  - type: background
    color: white (0)
    role: static
  - type: boundary
    description: A solid line (horizontal or vertical) of a single color.
    color: varies (yellow in ex1, green in ex2)
    role: static, acts as a barrier
  - type: mover
    description: A single, isolated pixel.
    color: varies (green in ex1, magenta in ex2)
    role: dynamic, moves towards the boundary
relationships:
  - mover pixel is initially separated from the boundary line by background pixels.
actions:
  - identify: Locate the boundary line.
  - identify: Locate the single mover pixel (distinct color from background and boundary).
  - determine_direction:
      if boundary is vertical:
        movement is horizontal (towards the boundary).
      if boundary is horizontal:
        movement is vertical (towards the boundary).
  - move: Relocate the mover pixel along the determined direction (row or column).
  - stop_condition: The mover pixel stops in the cell immediately adjacent to the boundary line along its path.
output_grid:
  - The background and boundary line remain unchanged from the input.
  - The mover pixel is placed in its final stopped position.
  - The original position of the mover pixel becomes background (white).
```


**Natural Language Program:**

1.  Identify the boundary object, which is a straight line (horizontal or vertical) of a single, non-white color.
2.  Identify the single 'mover' pixel, which has a color distinct from both the background (white) and the boundary line. Record its initial position (row, column) and color.
3.  Determine the direction of movement:
    *   If the boundary line is vertical (all its pixels share the same column index), the movement is horizontal towards that column.
    *   If the boundary line is horizontal (all its pixels share the same row index), the movement is vertical towards that row.
4.  Determine the target position:
    *   If moving horizontally towards a vertical boundary at column `C_boundary`: The target position is `(initial_row, C_boundary - 1)` if the mover starts left of the boundary, or `(initial_row, C_boundary + 1)` if the mover starts right of the boundary. (Based on examples, it seems movers start left/below, so it will be `C_boundary - 1` or `R_boundary + 1`).
    *   If moving vertically towards a horizontal boundary at row `R_boundary`: The target position is `(R_boundary + 1, initial_column)` if the mover starts below the boundary, or `(R_boundary - 1, initial_column)` if the mover starts above the boundary. (Based on examples, it will be `R_boundary + 1`).
5.  Create the output grid by copying the input grid.
6.  Set the pixel at the mover's initial position to white (0) in the output grid.
7.  Set the pixel at the calculated target position to the mover's color in the output grid.