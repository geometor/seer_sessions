
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 9 0 0 0
0 9 0 9 0
0 9 0 9 0
```


**output:**
```
0 0 0 0 0
3 3 3 0 0
3 9 3 3 3
0 9 3 9 3
0 9 0 9 0
```


## train_2

**input:**
```
0 0 0 0 0
0 0 9 0 0
0 0 9 0 0
0 0 9 0 0
0 0 9 0 9
```


**output:**
```
0 3 3 3 0
0 3 9 3 0
0 0 9 0 0
0 0 9 3 3
0 0 9 3 9
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
9 0 9 0 9
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
3 3 3 3 3
9 3 9 3 9
```

Okay, analyzing the provided examples.

**Perception of Elements:**

The task involves transforming a 2D grid (represented as a list of lists or similar structure) containing numerical values.
*   **Input Grid:** Composed of integers 0 and 9. The grid size appears consistent (5x5 in the examples).
*   **Output Grid:** Composed of integers 0, 3, and 9. The grid size is the same as the input.
*   **Transformation:** The core transformation involves changing some of the 0s in the input grid to 3s in the output grid. The 9s seem to remain unchanged. The placement of the new 3s appears related to the position of the 9s in the input grid. Specifically, 0s that are adjacent (including diagonals) to a 9 in the input grid become 3s in the output grid.

**YAML Facts:**


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2
  cell_type: integer
  size: 5x5 # based on examples, may vary
input_elements:
  - value: 0
    role: background / empty cell
  - value: 9
    role: source / influencer cell
output_elements:
  - value: 0
    role: background / empty cell (unchanged from input, not adjacent to 9)
  - value: 3
    role: affected cell (was 0 in input, adjacent to a 9)
  - value: 9
    role: source / influencer cell (unchanged from input)
transformation_rule:
  - action: copy_grid
    source: input
    target: output # Initialize output as a copy
  - action: iterate_cells
    target: input_grid
    condition: cell value is 0
    sub_action:
      - action: check_neighbors
        target: current_cell_in_input
        neighborhood: Moore (8 adjacent cells including diagonals)
        condition: any neighbor value is 9
        result_if_true: change corresponding output cell value to 3
relationships:
  - type: adjacency
    between: cell with value 0 (input) and cell with value 9 (input)
    effect: causes the 0 cell to become 3 in the output
  - type: identity
    between: cell with value 9 (input) and cell with value 9 (output)
    effect: value preserved
  - type: identity
    between: cell with value 0 (input, not adjacent to 9) and cell with value 0 (output)
    effect: value preserved
```


**Natural Language Program:**

1.  Create a new grid (the output grid) with the same dimensions as the input grid.
2.  Iterate through each cell (row `r`, column `c`) of the input grid.
3.  Get the value of the current cell in the input grid, let's call it `input_value`.
4.  **If `input_value` is 9:**
    *   Set the value of the corresponding cell (`r`, `c`) in the output grid to 9.
5.  **If `input_value` is 0:**
    *   Initialize a flag, `is_neighbor_9`, to false.
    *   Examine the 8 neighboring cells (horizontally, vertically, and diagonally adjacent) of the current cell (`r`, `c`) within the bounds of the *input* grid.
    *   For each valid neighbor:
        *   If the neighbor's value in the *input* grid is 9, set `is_neighbor_9` to true and stop checking neighbors for this cell.
    *   **If `is_neighbor_9` is true:**
        *   Set the value of the corresponding cell (`r`, `c`) in the output grid to 3.
    *   **If `is_neighbor_9` is false:**
        *   Set the value of the corresponding cell (`r`, `c`) in the output grid to 0.
6.  After iterating through all input cells, the output grid contains the final transformed result.
```python
import numpy as np
import copy

"""
Transforms an input grid based on the following rule:
1. Cells with value 9 remain unchanged.
2. Cells with value 0 are transformed to 3 if they are adjacent (horizontally, vertically, or diagonally) to a cell with value 9 in the input grid.
3. Cells with value 0 that are not adjacent to any 9 remain 0.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Get grid dimensions
    height, width = input_np.shape
    # Initialize the output grid as a deep copy of the input grid
    # This handles preserving the 9s and the initial state of 0s
    output_np = input_np.copy()

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* grid is 0
            if input_np[r, c] == 0:
                # Assume initially that no neighbor is 9
                is_neighbor_9 = False
                # Check all 8 neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is 9
                        if input_np[nr, nc] == 9:
                            is_neighbor_9 = True
                            # Found a 9 neighbor, no need to check others for this cell
                            break
                
                # If a neighbor was 9, change the corresponding cell in the *output* grid to 3
                if is_neighbor_9:
                    output_np[r, c] = 3
            # If the input cell was 9, it's already copied to output_np
            # If the input cell was 0 and had no 9 neighbors, it remains 0 in output_np

    # Convert the NumPy array back to a list of lists for the return value
    output_grid = output_np.tolist()
    return output_grid
```
