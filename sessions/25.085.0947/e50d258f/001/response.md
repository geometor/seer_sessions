```python
import numpy as np
from collections import deque

"""
Identify all contiguous blocks of non-white (non-zero) pixels using 4-connectivity (horizontal/vertical adjacency). 
For each block, determine its minimal bounding box. 
Find the unique block where the subgrid defined by its bounding box contains *only* non-white pixels (i.e., has a density of 1.0). 
The output is this subgrid.
"""

def find_connected_components(grid):
    """
    Finds all connected components of non-zero pixels in the grid.
    Uses 4-connectivity (horizontal/vertical).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-zero and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS to find all connected pixels in this component
                component = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is non-zero and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found component to the list
                components.append(component)
                
    return components

def get_bounding_box(component):
    """
    Calculates the bounding box (min_row, max_row, min_col, max_col) for a component.

    Args:
        component (list): A list of (row, col) tuples representing the component.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if component is empty.
    """
    if not component:
        return None
    # Extract all row and column indices
    rows = [r for r, c in component]
    cols = [c for r, c in component]
    # Find the min and max row and column indices
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by finding and extracting the unique dense subgrid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The extracted subgrid, or an empty list if no such subgrid is found.
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    
    # Handle empty grid case
    if grid.size == 0:
        return []

    # Find all connected components (blocks) of non-zero pixels
    components = find_connected_components(grid)

    # Initialize variable to store the target subgrid
    target_subgrid_list = []

    # Iterate through each found component
    for component in components:
        if not component:
            continue

        # Determine the bounding box for the current component
        bbox = get_bounding_box(component)
        min_row, max_row, min_col, max_col = bbox

        # Extract the subgrid corresponding to the bounding box
        # Numpy slicing is exclusive of the end index, so add 1 to max indices
        subgrid = grid[min_row : max_row + 1, min_col : max_col + 1]

        # Check if all pixels within this bounding box subgrid are non-zero (density is 1.0)
        if np.all(subgrid != 0):
            # If density is 1.0, this is our target subgrid
            # Convert the numpy subgrid back to a list of lists
            target_subgrid_list = subgrid.tolist()
            # Assume uniqueness based on examples and break the loop
            break 

    # Return the found target subgrid
    return target_subgrid_list
```