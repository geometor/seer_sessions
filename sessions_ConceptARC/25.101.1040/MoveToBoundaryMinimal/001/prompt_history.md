
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 3 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 3 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


## train_2

**input:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task involves moving a single colored pixel within a grid towards a static boundary line. The grid background is white (0). There are two distinct colored objects in the input: a single pixel (the "mover") and a line of pixels along one edge (the "boundary"). The boundary line remains unchanged in the output. The mover pixel changes its position, moving in a straight line (either horizontally or vertically) until it is immediately adjacent to the boundary line. The direction of movement is perpendicular to the orientation of the boundary line. If the boundary is vertical, the mover moves horizontally. If the boundary is horizontal, the mover moves vertically. The mover retains its original color.

**YAML Facts:**


```yaml
task_description: Move a single pixel towards a boundary line until adjacent.
components:
  - type: grid
    properties:
      background_color: white (0)
      size: variable (e.g., 10x10 in examples)
  - type: object
    id: boundary_line
    properties:
      shape: line (horizontal or vertical)
      location: along one edge of the grid (top or right in examples)
      color: variable (yellow or green in examples)
      static: true
  - type: object
    id: moving_pixel
    properties:
      shape: single pixel
      location: somewhere within the grid, not on the boundary
      color: variable (green or magenta in examples), different from boundary
      static: false
actions:
  - action: move
    target: moving_pixel
    constraints:
      - type: direction
        value: perpendicular to the boundary_line orientation (horizontal towards vertical boundary, vertical towards horizontal boundary)
      - type: destination
        value: position immediately adjacent to the boundary_line
      - type: path
        value: straight line
      - type: preserve_coordinate
        value: the coordinate parallel to the boundary_line remains unchanged
relationships:
  - type: adjacency
    object1: moving_pixel (final position)
    object2: boundary_line
    condition: directly adjacent (sharing an edge)
```


**Natural Language Program:**

1.  Identify the background color (white).
2.  Identify the boundary line object: a contiguous line of pixels of the same color located along one edge of the input grid. Note its color, location (which edge), and orientation (horizontal or vertical).
3.  Identify the moving pixel object: a single pixel with a color different from both the background and the boundary line. Note its color and initial position (row, column).
4.  Initialize the output grid as a copy of the input grid.
5.  Erase the moving pixel from its original position in the output grid (set the cell to the background color).
6.  Determine the target position for the moving pixel:
    *   If the boundary line is vertical (e.g., along the rightmost column `C`): The target position has the same row as the moving pixel's original row, and its column is `C-1` (immediately to the left of the boundary).
    *   If the boundary line is horizontal (e.g., along the topmost row `R`): The target position has the same column as the moving pixel's original column, and its row is `R+1` (immediately below the boundary).
    *   *(Generalize for other edges if necessary: left boundary -> target col = boundary_col + 1; bottom boundary -> target row = boundary_row - 1)*
7.  Place the moving pixel (with its original color) at the calculated target position in the output grid.
8.  The boundary line remains in its original position.
