
## train_1

**input:**
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```


**output:**
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 8 8
3 0 0 4 0 6
1 1 5 5 0 6
2 2 2 2 2 2
```


## train_3

**input:**
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are 2D grids of colored pixels.
2.  **Background Color:** The predominant background color is white (0).
3.  **Objects:** There are contiguous blocks of non-white colors. These appear to be the objects being manipulated.
4.  **Special Color:** The color red (2) appears consistently in each example, forming a solid line (either a full row or a full column).
5.  **Transformation:** The core transformation seems to be a movement or shifting of the non-white, non-red objects. The direction of movement is related to the position of the red line. Objects move towards the red line and stop when they hit it or another object that has already stopped. The space previously occupied by the moved objects becomes white.
6.  **Boundary Behavior:** The red line acts as a static boundary or wall. Objects move towards it but do not cross or displace it.
7.  **Gravity/Packing:** The objects seem to "fall" or "slide" towards the red line, packing together against it and against each other in the direction of movement.

**YAML Facts:**


```yaml
task_type: object_manipulation
components:
  - role: background
    color: white (0)
    properties: static, fills vacated space
  - role: boundary
    color: red (2)
    shape: solid line (row or column)
    properties: static, immovable, defines movement direction
  - role: movable_objects
    color: any color except white (0) and red (2)
    shape: contiguous blocks of single color
    properties: mobile
actions:
  - name: identify_boundary
    input: input_grid
    output: red line coordinates, orientation (horizontal/vertical), position (top/bottom/left/right)
  - name: determine_movement_direction
    input: boundary position and orientation
    output: direction vector (e.g., down, up, left, right) - always towards the boundary
  - name: shift_objects
    input: input_grid, boundary, movement_direction
    output: output_grid
    process:
      - Initialize output grid based on input dimensions.
      - Copy the red boundary line from input to output.
      - Fill the rest of the output grid with white.
      - Iterate through the input grid cells (excluding the boundary).
      - For each non-white, non-red pixel found:
        - Determine its target position by moving it in the movement_direction until it hits:
          - The cell adjacent to the red boundary.
          - A cell adjacent to a non-white pixel already placed in the output grid.
        - Place the pixel's color at the calculated target position in the output grid.
relationships:
  - type: spatial
    description: Movable objects are positioned relative to the red boundary.
  - type: interaction
    description: Movable objects shift towards the red boundary until collision with the boundary or another previously shifted object.
```


**Natural Language Program:**

1.  **Identify the Boundary Line:** Find the solid line (row or column) composed entirely of red (2) pixels in the input grid. Note its orientation (horizontal or vertical) and position (e.g., row index 9, column index 0).
2.  **Determine Movement Direction:**
    *   If the boundary is a column on the left (index 0), the direction is left.
    *   If the boundary is a column on the right (max column index), the direction is right.
    *   If the boundary is a row at the top (index 0), the direction is up.
    *   If the boundary is a row at the bottom (max row index), the direction is down.
3.  **Initialize Output Grid:** Create a new grid with the same dimensions as the input grid.
4.  **Copy Boundary:** Copy the red boundary line from the input grid to the corresponding location in the new output grid.
5.  **Initialize Background:** Fill all other cells in the new output grid with white (0).
6.  **Shift Objects Towards Boundary:** Iterate through each cell of the *input* grid. If a cell contains a color other than white (0) or red (2):
    *   Starting from the cell's original position, trace a path one step at a time in the determined movement direction.
    *   Stop tracing at the final position, which is the cell *just before* you would encounter:
        *   The red boundary line.
        *   A cell in the *output* grid that is already occupied by a non-white color (meaning another object has already settled there).
    *   Place the color from the original input cell into this final position in the *output* grid.
7.  **Return Output:** The completed new grid is the result.
```python
import numpy as np

"""
Identifies a solid red (2) line (row or column) acting as a boundary.
All other non-white (0) objects are shifted towards this boundary.
The shifting continues until an object reaches the cell adjacent to the boundary 
or the cell adjacent to another object that has already been shifted and settled.
The space vacated by the shifted objects becomes white (0).
The red boundary itself remains static.
"""

def find_boundary(grid: np.ndarray) -> tuple[str | None, int | None]:
    """
    Finds a solid red line (row or column).

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (orientation, index) where orientation is 'row' or 'col',
        and index is the row/column index. Returns (None, None) if no boundary found.
    """
    height, width = grid.shape
    red_color = 2

    # Check rows
    for r in range(height):
        if np.all(grid[r, :] == red_color):
            return 'row', r

    # Check columns
    for c in range(width):
        if np.all(grid[:, c] == red_color):
            return 'col', c

    return None, None

def determine_direction(orientation: str, index: int, height: int, width: int) -> tuple[int, int] | None:
    """
    Determines the direction vector (dr, dc) towards the boundary.

    Args:
        orientation: 'row' or 'col'.
        index: The index of the boundary row/column.
        height: Grid height.
        width: Grid width.

    Returns:
        A tuple (dr, dc) representing the movement direction (e.g., (-1, 0) for up),
        or None if orientation is invalid.
    """
    if orientation == 'row':
        if index == 0:  # Top boundary, move up
            return (-1, 0)
        elif index == height - 1: # Bottom boundary, move down
            return (1, 0)
    elif orientation == 'col':
        if index == 0:  # Left boundary, move left
            return (0, -1)
        elif index == width - 1: # Right boundary, move right
            return (0, 1)
    # Should not happen with valid boundaries, but good practice
    return None # Or perhaps default to down (1, 0)? Example 1 has bottom row implicit boundary? No, the red is explicit.


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Shifts non-white, non-red objects towards a solid red boundary line until
    they hit the boundary or another settled object.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    white_color = 0
    red_color = 2

    # Find the boundary
    orientation, boundary_index = find_boundary(input_np)

    if orientation is None:
        # Handle cases where no boundary is found (though examples suggest one always exists)
        # Maybe return input unchanged or raise an error? Returning unchanged for now.
        return input_grid

    # Determine movement direction
    dr, dc = determine_direction(orientation, boundary_index, height, width)

    # Initialize output grid with white
    output_np = np.full_like(input_np, white_color)

    # Copy the boundary to the output grid
    if orientation == 'row':
        output_np[boundary_index, :] = red_color
    else: # orientation == 'col'
        output_np[:, boundary_index] = red_color

    # Determine iteration order based on direction to process objects closer to the boundary first
    rows = range(height)
    cols = range(width)

    if dr > 0: # Moving down
        rows = range(height - 1, -1, -1)
    elif dr < 0: # Moving up
        rows = range(height) # Default order is fine
    
    if dc > 0: # Moving right
        cols = range(width - 1, -1, -1)
    elif dc < 0: # Moving left
        cols = range(width) # Default order is fine

    # Iterate through input grid cells based on calculated order
    for r in rows:
        for c in cols:
            color = input_np[r, c]

            # Skip background, boundary, and already processed parts of the output grid
            if color == white_color or color == red_color:
                continue

            # This pixel belongs to a movable object
            current_r, current_c = r, c

            # Simulate movement step-by-step until collision
            while True:
                next_r, next_c = current_r + dr, current_c + dc

                # Check boundary conditions
                if not (0 <= next_r < height and 0 <= next_c < width):
                    break # Hit grid edge (shouldn't happen before hitting boundary)

                # Check collision with boundary or already settled object in output
                if output_np[next_r, next_c] != white_color:
                     break # Hit boundary or another object

                # Move is valid, update current position
                current_r, current_c = next_r, next_c

            # Place the object's color at the final settled position
            output_np[current_r, current_c] = color

    # Convert back to list of lists
    output_grid = output_np.tolist()
    return output_grid
```
