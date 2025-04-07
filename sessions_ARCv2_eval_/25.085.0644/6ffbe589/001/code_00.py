import numpy as np
from collections import deque

"""
Identifies the largest connected component of non-white pixels (value > 0) in the input grid, considering 8-way connectivity (including diagonals). 
Then, it crops the input grid to the minimal bounding box containing this largest component.
"""

def find_connected_components(grid_np):
    """
    Finds all connected components of non-white pixels in the grid.

    Args:
        grid_np (np.array): The input grid as a numpy array.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid_np.shape
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited yet, start BFS
            if grid_np[r, c] != 0 and (r, c) not in visited:
                component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    component.append((row, col))

                    # Check 8 neighbors (horizontal, vertical, diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip self

                            nr, nc = row + dr, col + dc

                            # Check boundaries
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is non-white and not visited
                                if grid_np[nr, nc] != 0 and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))
                
                components.append(component)
                
    return components

def transform(input_grid):
    """
    Identifies the largest connected component of non-white pixels and crops the grid to its bounding box.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The cropped output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Find all connected components of non-white pixels
    components = find_connected_components(input_grid_np)

    # Handle case where there are no non-white pixels
    if not components:
        # Return a minimal representation, e.g., a 1x1 white grid, or perhaps the original grid.
        # Let's return a 1x1 white grid based on typical ARC behavior for "empty" outputs.
        return [[0]] 

    # Find the largest component (by number of pixels)
    largest_component = max(components, key=len)

    # If the largest component is empty (shouldn't happen if components is not empty, but good practice)
    if not largest_component:
         return [[0]]

    # Calculate the bounding box of the largest component
    rows = [r for r, c in largest_component]
    cols = [c for r, c in largest_component]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Crop the original grid using the bounding box coordinates
    # Slicing is [start_row:end_row+1, start_col:end_col+1]
    output_grid_np = input_grid_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid