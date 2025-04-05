
## train_1

**input:**
```
0 3 0 0 3
0 0 3 0 0
3 0 0 0 3
3 0 0 3 3
0 0 0 0 0
```


**output:**
```
0 3 0 0 3
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 3 3 3 0
3 0 0 0 0
3 0 3 0 3
3 0 3 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 3
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 3
0 0 0 3 0
0 0 3 0 0
0 3 0 0 0
0 0 0 0 3
```


**output:**
```
0 0 0 0 3
0 0 0 3 0
0 0 3 0 0
0 3 0 0 0
0 0 0 0 3
```


## train_4

**input:**
```
0 3 3 3 3
0 0 3 0 3
0 0 0 0 0
0 0 3 3 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

*   **Perception of the Elements:**
    *   The inputs and outputs are 5x5 grids containing integers 0 and 3.
    *   The transformation involves selectively keeping or removing the '3's based on their spatial arrangement in the input grid.
    *   Cells containing '0' in the input generally remain '0' in the output, unless they were part of a group of '3's that gets removed.
    *   The key factor appears to be the connectivity of the '3's. '3's that are adjacent (horizontally, vertically, or diagonally) form connected components.
    *   The transformation retains only those '3's that are isolated, meaning they are not adjacent (including diagonally) to any other '3'. All other '3's (those part of components larger than one cell) are turned into '0's.

*   **Facts:**
    
```yaml
    objects:
      - grid:
          description: A 2-dimensional array (5x5) representing the input and output state.
          properties:
            - dimensions: [5, 5]
            - cell_values: [0, 3]
      - cell:
          description: An individual element within the grid.
          properties:
            - value: 0 or 3
            - position: (row, column) coordinates
            - neighbors: Adjacent cells (horizontally, vertically, and diagonally)
      - connected_component:
          description: A group of cells containing the value '3' where each cell is connected to at least one other cell in the group through horizontal, vertical, or diagonal adjacency.
          properties:
            - cells: List of cell positions belonging to the component.
            - size: The number of cells in the component.
    actions:
      - identify_components:
          description: Find all connected components of cells with value '3' in the input grid, using 8-way adjacency (including diagonals).
      - filter_components:
          description: Select components based on a specific property. In this task, the property is size.
          criteria: Keep only components where size is equal to 1.
      - generate_output:
          description: Create the output grid. Cells that were part of the kept components retain their value '3'. All other cells are set to '0'.
    relationships:
      - A cell belongs to at most one connected_component.
      - The output grid is derived from the input grid by applying the identify_components, filter_components, and generate_output actions sequentially.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled with zeros.
    2.  Identify all connected components of cells containing the value '3' in the input grid. Consider cells to be connected if they are adjacent horizontally, vertically, or diagonally (8-way connectivity).
    3.  For each identified connected component:
        a.  Determine the size of the component (the number of '3's it contains).
        b.  If the size of the component is exactly 1, then locate the position of that single '3' in the input grid and set the corresponding cell in the output grid to '3'.
    4.  Return the generated output grid.
```python
import numpy as np
from collections import deque

"""
Transforms a 5x5 grid of 0s and 3s by keeping only the '3's that are isolated.
A '3' is considered isolated if it has no adjacent '3's horizontally, vertically, or diagonally (8-way connectivity).
This is achieved by finding all connected components of '3's and only retaining components of size 1.
"""

def get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors for a cell. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid):
    """ Finds all connected components of '3's using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If we find an unvisited '3', start a BFS to find its component
            if grid[r, c] == 3 and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Explore neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr, nc] == 3 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found component
                components.append(current_component)
                
    return components

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Keeps only '3's that form a connected component of size 1.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Find all connected components of '3's
    components = find_connected_components(input_array)

    # Filter components: keep only those with size 1
    for component in components:
        if len(component) == 1:
            # Get the coordinates of the isolated '3'
            r, c = component[0]
            # Set the corresponding cell in the output grid to '3'
            output_grid[r, c] = 3
            
    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()

```
