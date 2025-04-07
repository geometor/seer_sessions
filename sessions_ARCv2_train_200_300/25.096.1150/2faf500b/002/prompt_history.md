
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 6 9 9 9 0 0
0 0 0 0 9 9 9 6 9 9 0 0
0 0 0 0 9 9 6 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 6 9 9 0 0 9 9 0
0 9 9 6 9 9 9 0 0 9 6 0
0 9 9 9 6 9 9 0 0 6 9 0
0 0 0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 9 9 9 0
0 0 0 9 9 9 0 0 0 9 9 0
0 0 0 9 9 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 9 0
9 9 9 0 0 0 9 9 0 9 0 0
9 9 0 0 0 9 9 9 0 0 0 0
9 9 9 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 9 9 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0
0 9 9 9 0 0 0 0
0 6 9 6 0 0 0 0
0 9 6 9 0 0 0 0
0 9 9 9 0 0 0 0
0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 0 0 0
0 9 9 9 0 0 0 0
0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0
0 9 9 9 0 0 0 0
0 9 9 9 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 6 9 0 0 9 9 9 9
0 0 0 0 0 0 9 6 9 9 0 0 9 9 9 9
0 0 9 9 0 0 0 0 0 0 0 0 9 9 9 9
0 0 6 9 0 0 0 0 0 0 0 0 9 6 9 6
0 0 9 6 0 0 0 0 0 0 0 0 6 9 6 9
0 0 9 9 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 6 9 9 9 0 0 0 0 0 0
0 0 9 9 9 6 9 9 9 9 0 0 0 0 0 0
0 0 9 9 9 9 6 9 9 9 0 0 0 0 0 0
0 0 9 9 9 6 9 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 9 9 0 0 0 9 0 9 9 9 9
0 0 9 9 0 9 0 0 0 9 9 0 9 9 9 9
0 0 0 9 0 0 0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 9 0 9
0 0 9 9 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 9 9 9 9 0 0 0 9 9 9 0 0 0 0 0
0 9 9 9 0 0 0 9 9 9 9 0 0 0 0 0
0 9 9 9 9 0 0 0 9 9 9 0 0 0 0 0
0 9 9 9 0 0 0 9 9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a 2D grid of digits.
*   **Grid:** The fundamental structure is a grid containing single-digit integers.
*   **Background:** The digit 0 represents the background or empty space.
*   **Shapes:** The digit 9 appears to form distinct shapes or regions within the grid.
*   **Markers:** The digit 6 acts as a marker, always appearing within or on the boundary of the '9' shapes.
*   **Transformation:** The core transformation involves modifying the '9' shapes based on the location of the '6' markers. Specifically, the '6' markers themselves and the '9's immediately adjacent (horizontally or vertically) to them are removed (turned into 0s). Other '9's and all '0's remain unchanged.

## YAML Facts


```yaml
elements:
  - object: grid
    properties:
      - type: 2D array
      - content: single digits (0-9)
  - object: cell
    properties:
      - value: digit (0, 6, 9 are significant)
      - location: (row, column) coordinates
  - object: background
    represented_by:
      - cell value: 0
  - object: shape_component
    represented_by:
      - cell value: 9
  - object: marker
    represented_by:
      - cell value: 6
    relationship:
      - type: located_within_or_adjacent_to
        target: shape_component (9)
actions:
  - action: identify
    target: cells with value 6
  - action: identify
    target: cells with value 9 that are adjacent (up, down, left, right) to cells with value 6
  - action: replace_value
    target: identified cells (both original 6s and adjacent 9s)
    new_value: 0
  - action: copy_value
    target: all other cells (original 0s and 9s not adjacent to 6s)
    condition: cell value was not identified for replacement
relationships:
  - type: adjacency
    between: cells (sharing an edge)
    relevance: determines which 9s are affected by a 6
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Create a list of coordinates for all cells in the input grid that contain the value 6.
3.  Create a second list to store the coordinates of cells to be changed to 0. Add all coordinates from the list created in step 2 to this second list.
4.  Iterate through each coordinate `(r, c)` identified in step 2 (where the input value is 6).
5.  For each such coordinate `(r, c)`, examine its four direct neighbors (up, down, left, right): `(r-1, c)`, `(r+1, c)`, `(r, c-1)`, `(r, c+1)`.
6.  If a neighbor exists within the grid boundaries *and* its value in the *input* grid is 9, add the coordinates of that neighbor to the list created in step 3.
7.  Iterate through all unique coordinates collected in the list from step 3.
8.  For each coordinate `(r_change, c_change)` in this list, set the value of the corresponding cell in the *output* grid to 0.
9.  The final output grid contains the transformed data.
```python
import numpy as np
from typing import List, Tuple, Set

"""
Transforms an input grid by finding all cells with the value 6. 
These '6' cells, along with any adjacent (up, down, left, right) cells containing the value 9, 
are then set to 0 in the output grid. All other cell values are copied directly from the input to the output.
"""

def _find_value_locations(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all locations (row, col) of a specific value in the grid."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def _get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets valid neighbor coordinates (up, down, left, right) for a given cell."""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: zeros out cells with value 6 and 
    any adjacent 9s.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_array = input_array.copy()

    # Find locations of all '6' markers
    marker_locations = _find_value_locations(input_array, 6)

    # Create a set to store coordinates of cells to be changed to 0
    # Using a set automatically handles duplicates
    coords_to_zero: Set[Tuple[int, int]] = set()

    # Add all marker locations to the set
    for r, c in marker_locations:
        coords_to_zero.add((r, c))

    # Iterate through each marker location
    for r, c in marker_locations:
        # Examine its neighbors
        neighbors = _get_neighbors(r, c, height, width)
        for nr, nc in neighbors:
            # If a neighbor is a '9' in the original input grid, add it to the set
            if input_array[nr, nc] == 9:
                coords_to_zero.add((nr, nc))

    # Iterate through the collected coordinates and set the corresponding cells in the output grid to 0
    for r_change, c_change in coords_to_zero:
        output_array[r_change, c_change] = 0

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
