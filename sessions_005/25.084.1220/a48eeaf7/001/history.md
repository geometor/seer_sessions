
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0
0 5 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 2 2 0 0 0
0 0 0 0 5 2 2 0 0 0
0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 5 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 2 2 5 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided task examples.

**Perception**

1.  **Grid Structure:** Both input and output grids are 10x10. The background color is white (0).
2.  **Objects:**
    *   In each input grid, there is a single contiguous red (2) object (a 2x2 square in these examples).
    *   There are also several individual gray (5) pixels scattered across the grid.
3.  **Transformation:**
    *   The red object remains unchanged in shape, color, and position between the input and output grids.
    *   The gray pixels change their positions from the input to the output.
    *   In the output, the gray pixels appear to be closer to the red object than they were in the input.
    *   Observing the movement path, each gray pixel seems to move step-by-step towards the nearest point on the red object.
    *   The movement stops when the gray pixel lands on a cell that is adjacent (including diagonals) to any part of the red object.
4.  **Color Consistency:** The colors of the objects (red and gray) remain the same; only the positions of the gray pixels change.

**Facts**


```yaml
task_description: Move gray pixels towards the nearest part of a static red object until they become adjacent to it.

elements:
  - type: grid
    properties:
      size: [10, 10] # Variable, but 10x10 in examples
      background_color: white (0)

  - type: object
    id: static_object
    properties:
      color: red (2)
      shape: contiguous block (2x2 square in examples)
      static: true # Does not change position or shape

  - type: object
    id: moving_objects
    properties:
      color: gray (5)
      shape: single pixel
      count: variable (4 in train_1, 3 in train_2)
      static: false # Changes position

relationships:
  - type: spatial
    description: Moving objects (gray) are initially scattered relative to the static object (red).
  - type: distance
    description: The transformation minimizes the Manhattan distance between each moving object and the static object, subject to a stopping condition.

actions:
  - action: identify
    actor: system
    target: static_object (red)
    details: Locate all pixels belonging to the red object.
  - action: identify
    actor: system
    target: moving_objects (gray)
    details: Locate all gray pixels.
  - action: calculate_path
    actor: system
    target: each moving_object
    details:
      - Find the nearest pixel(s) on the static_object using Manhattan distance.
      - Determine the step direction (dx, dy) towards a chosen nearest static_object pixel.
  - action: move
    actor: system
    target: each moving_object
    details:
      - Iteratively move the gray pixel one step in the calculated direction.
      - Stop when the pixel's current position is adjacent (including diagonals) to any pixel of the static_object.
      - Adjacency means the maximum of the absolute difference in row and column indices is 1.
  - action: update_grid
    actor: system
    target: output_grid
    details:
      - Copy the input grid.
      - Remove the original moving_objects.
      - Place the moving_objects at their calculated final positions.
      - Ensure the static_object remains unchanged.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all pixels belonging to the static red (2) object and store their coordinates.
3.  Identify all gray (5) pixels in the input grid and store their initial coordinates.
4.  For each identified gray pixel:
    a.  Remove the gray pixel from its original position in the output grid (set it to white (0)).
    b.  Calculate the Manhattan distance from the gray pixel's initial position to every red pixel identified in step 2.
    c.  Find the minimum Manhattan distance calculated.
    d.  Identify the target red pixel(s) that correspond to this minimum distance. If there are multiple, select one consistently (e.g., the one with the smallest row index, then the smallest column index).
    e.  Set the gray pixel's current position to its initial position.
    f.  Start a movement loop:
        i.  Check if the gray pixel's current position is adjacent (including diagonals) to *any* red pixel. Two pixels (r1, c1) and (r2, c2) are adjacent if `max(abs(r1-r2), abs(c1-c2)) == 1`.
        ii. If the current position *is* adjacent to a red pixel, exit the movement loop.
        iii. If the current position is *not* adjacent, calculate the next step direction towards the target red pixel:
            *   `dx = 0` if `target_row == current_row`, `1` if `target_row > current_row`, `-1` if `target_row < current_row`.
            *   `dy = 0` if `target_col == current_col`, `1` if `target_col > current_col`, `-1` if `target_col < current_col`.
        iv. Update the gray pixel's current position by adding `dx` to the row and `dy` to the column.
    g.  After the loop terminates, place the gray (5) color at the final `(current_row, current_col)` position in the output grid.
5.  Return the modified output grid.
