
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
2 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
2 2 2 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 4 3 3 3
0 0 0 4 4 3 3 3
0 0 0 0 0 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0
0 0 0 4 4 4 4 0
0 0 0 4 3 3 3 0
0 0 0 4 3 3 3 0
0 0 0 0 3 3 3 0
```


## train_3

**input:**
```
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0
4 4 4 0 0 0 0 0
4 4 4 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 5 1 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 1 5 5 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Perception

1.  **Input/Output Format:** The task takes an 8x8 grid of single-digit integers as input and produces another 8x8 grid of integers as output.
2.  **Grid Contents:** The grids contain the digit 0, representing a background or empty space, and other non-zero digits (1, 2, 3, 4, 5, 6 in the examples) representing distinct "colors" or "objects". These non-zero digits often form connected components or shapes.
3.  **Core Transformation:** The transformation involves spatial rearrangement of some colored shapes based on their interaction with horizontally adjacent shapes of different colors.
4.  **Interaction Rule:** The key interaction occurs between horizontally adjacent cells with different non-zero values. Let `V1` be the value of a cell `(r, c)` and `V2` be the value of its right neighbor `(r, c+1)`. If `V1 > 0`, `V2 > 0`, and `V1 != V2`, an interaction occurs.
5.  **Movement Trigger:** The interaction triggers a movement (shift) of the entire connected component associated with the *smaller* value between `V1` and `V2`.
6.  **Movement Direction:** The triggered movement is always one step to the *left*.
7.  **Overwriting:** When a shape shifts left, its constituent cells overwrite the contents of the destination cells in the grid. The original positions of the shifted shape become empty (0), unless overwritten by another shape.
8.  **Simultaneity:** The decision of which shapes to move seems based on all relevant adjacencies present in the *input* grid. All identified shifts are then applied to generate the output grid. A shape might be involved in multiple adjacencies (e.g., Example 4, the '1' is adjacent to '5' on both left and right), but the outcome (shifting the component with the minimum value left) remains consistent.
9.  **Stability:** Shapes that are not identified for movement remain in their original positions, unless overwritten by a moving shape. Background cells (0) also remain unchanged unless overwritten.

## Facts


```yaml
Objects:
  - Grid: An 8x8 matrix of integer values.
  - Cell: A single position (row, column) within the grid, holding an integer value.
  - Shape: A connected component of cells sharing the same non-zero integer value. Connectivity is likely 4-directional (up, down, left, right).
  - Background: Cells with the value 0.

Properties:
  - Cell:
    - position: (row, column) coordinates.
    - value: Integer digit (0-9).
  - Shape:
    - value: The non-zero integer shared by all cells in the shape.
    - cells: A set of coordinates representing the cells belonging to the shape.
    - bounding_box: (Optional) Min/max row/column occupied by the shape.

Actions:
  - Identify Shapes: Find all connected components of non-zero cells in the input grid.
  - Check Horizontal Adjacency: For each cell (r, c), check its right neighbor (r, c+1).
  - Compare Values: If cell (r, c) has value V1 > 0 and cell (r, c+1) has value V2 > 0, compare V1 and V2.
  - Determine Minimum Value Shape: If V1 != V2, identify the shape associated with min(V1, V2).
  - Mark for Shifting: Mark the identified minimum value shape for a leftward shift.
  - Shift Shape Left:
    - Clear Original Positions: Set the value of the original cells of the shifted shape to 0 in the output grid.
    - Set New Positions: Set the value of the cells one column to the left of the original positions to the shape's value in the output grid, overwriting existing values.
  - Copy Unchanged: Transfer cells not involved in shifts or overwriting from input to output.

Relationships:
  - Adjacency: Cells are adjacent horizontally if they are in the same row and adjacent columns.
  - Belonging: A cell belongs to a specific shape if it has the shape's value and is connected to other cells of that shape.
  - Comparison: Values of adjacent non-zero cells are compared (V1 vs V2).
  - Trigger: The condition V1 > 0, V2 > 0, V1 != V2 between horizontally adjacent cells triggers a potential shift.
  - Shift Target: The shape with the minimum value (min(V1, V2)) is the target for the leftward shift.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all connected components (shapes) of non-zero values in the input grid. Keep track of which cells belong to which shape and the value associated with each shape.
3.  Create a set to store the shapes that need to be shifted left.
4.  Iterate through each cell `(r, c)` of the input grid from `r = 0` to `7` and `c = 0` to `6`.
5.  Let `V1` be the value of the cell `(r, c)` and `V2` be the value of the cell `(r, c+1)`.
6.  If both `V1` and `V2` are non-zero and `V1` is not equal to `V2`:
    a.  Determine the minimum value: `V_min = min(V1, V2)`.
    b.  Identify the shape `S_min` whose value is `V_min` and which contains either cell `(r, c)` (if `V1 == V_min`) or cell `(r, c+1)` (if `V2 == V_min`).
    c.  Add the identified shape `S_min` to the set of shapes to be shifted.
7.  Iterate through each shape `S` in the set of shapes identified for shifting:
    a.  Let `V_S` be the value of shape `S`.
    b.  For every cell `(r, c)` that belongs to shape `S`:
        i.  Set the value of cell `(r, c)` in the *output grid* to 0 (clear the original position).
    c.  For every cell `(r, c)` that belongs to shape `S`:
        i.  If `c > 0`, set the value of cell `(r, c-1)` in the *output grid* to `V_S` (set the new shifted position, overwriting whatever was there). Handle boundary conditions (cannot shift left from column 0).
8.  Return the final output grid.
```python
import numpy as np
from collections import deque

"""
Identify connected components (shapes) of non-zero values in the input grid.
Check for horizontal adjacencies between cells of different non-zero values.
If two adjacent cells (r, c) and (r, c+1) have values V1 and V2 (both > 0, V1 != V2), 
identify the shape associated with the minimum value (min(V1, V2)).
Mark this minimum-value shape for a leftward shift (move one column to the left).
Apply all identified shifts simultaneously: 
  - First, clear the original positions of all shifting shapes in the output grid.
  - Second, fill the new, left-shifted positions of all shifting shapes in the output grid, overwriting existing values.
Shapes not marked for shifting remain in place unless overwritten by a shifting shape.
"""

def _find_shapes(grid):
    """
    Identifies all connected components (shapes) of non-zero values using BFS.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - shapes: A dictionary mapping shape_id to {'value': int, 'cells': set((r, c))}.
        - cell_to_shape_id: A numpy array of the same shape as grid, where each cell 
                           contains the shape_id it belongs to, or -1 if background (0).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    cell_to_shape_id = np.full((rows, cols), -1, dtype=int)
    shapes = {}
    shape_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not visited yet, start a BFS
            if grid[r, c] != 0 and not visited[r, c]:
                value = grid[r, c]
                current_shape_id = shape_id_counter
                shapes[current_shape_id] = {'value': value, 'cells': set()}
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    # Add cell to the current shape
                    shapes[current_shape_id]['cells'].add((row, col))
                    cell_to_shape_id[row, col] = current_shape_id

                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check boundaries, if neighbor has the same value, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == value and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                shape_id_counter += 1
                
    return shapes, cell_to_shape_id

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Identifies shapes based on horizontal adjacency of different non-zero colors.
    Shifts the shape with the minimum value in such adjacent pairs one step to the left.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = grid.copy() # Initialize output grid as a copy

    # 1. Identify all shapes in the input grid
    shapes, cell_to_shape_id = _find_shapes(grid)
    
    # 2. Identify shapes to shift based on horizontal adjacency
    shapes_to_shift_ids = set()
    for r in range(rows):
        for c in range(cols - 1): # Iterate up to the second-to-last column
            v1 = grid[r, c]
            v2 = grid[r, c + 1]

            # Check for horizontal adjacency between different non-zero values
            if v1 != 0 and v2 != 0 and v1 != v2:
                # Determine the minimum value and the corresponding shape_id
                if v1 < v2:
                    min_val_shape_id = cell_to_shape_id[r, c]
                else: # v2 < v1
                    min_val_shape_id = cell_to_shape_id[r, c + 1]
                
                # Add the shape_id to the set of shapes to be shifted
                # Check if min_val_shape_id is valid (not -1) before adding
                if min_val_shape_id != -1:
                    shapes_to_shift_ids.add(min_val_shape_id)

    # 3. Apply the shifts (in two phases to handle overlaps correctly)
    
    # Phase 1: Clear the original positions of shifting shapes
    for shape_id in shapes_to_shift_ids:
        shape_info = shapes[shape_id]
        for r, c in shape_info['cells']:
            output_grid[r, c] = 0 # Set original cell to background

    # Phase 2: Fill the new, left-shifted positions
    for shape_id in shapes_to_shift_ids:
        shape_info = shapes[shape_id]
        shape_value = shape_info['value']
        for r, c in shape_info['cells']:
            # Check if the shift is possible (not shifting from column 0)
            if c > 0:
                new_c = c - 1
                output_grid[r, new_c] = shape_value # Set new cell value, overwriting if necessary

    return output_grid.tolist() # Return as list of lists per standard format
```
