```python
import numpy as np
from collections import deque

def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in a grid using BFS.
    Connectivity is defined as 4-directional (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the components to find.

    Returns:
        list: A list of lists, where each inner list contains the
              (row, col) coordinates of the pixels in a connected component.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If this pixel is the target color and hasn't been visited yet,
            # start a BFS to find its connected component.
            if grid[r, c] == target_color and not visited[r, c]:
                component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add the found component to the list of components
                if component:
                    components.append(component)

    return components

def transform(input_grid):
    """
    Identifies the primary non-background color in the input grid.
    Finds all distinct connected components of this primary color.
    Calculates the size of each component and selects the largest one.
    Creates a new output grid containing only the pixels of the largest component,
    setting all other pixels to the background color (0).
    """
    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    background_color = 0
    
    # 1. Identify the primary non-background color
    primary_color = None
    unique_colors = np.unique(input_np)
    for color in unique_colors:
        if color != background_color:
            primary_color = color
            break # Assume only one non-background color based on examples

    # If no non-background color is found, return a grid of background color
    if primary_color is None:
        return np.zeros_like(input_np).tolist() # Return as list of lists if needed

    # 2. Find all distinct connected components of the primary color
    components = find_connected_components(input_np, primary_color)

    # If no components are found, return a grid of background color
    if not components:
         return np.zeros_like(input_np).tolist()

    # 3. Calculate the size of each component and find the largest one
    largest_component = []
    max_size = 0
    for component in components:
        if len(component) > max_size:
            max_size = len(component)
            largest_component = component
        # Handle ties: the first largest component found is kept (consistent with description)

    # 5. Create a new output grid initialized with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # 6. Copy the pixels belonging to the largest component to the output grid
    for r, c in largest_component:
        output_grid[r, c] = primary_color

    return output_grid.tolist() # Return as list of lists
```