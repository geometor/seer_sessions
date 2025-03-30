```python
import numpy as np
from collections import deque

"""
Identify all non-white pixels in the input grid.
Find the largest connected component among these non-white pixels (using orthogonal adjacency). 
This component represents the main rectangular object, including its border and internal contents.
Determine the bounding box (minimum row, minimum column, maximum row, maximum column) of this largest connected component.
Extract the subgrid from the input grid defined by this bounding box.
The extracted subgrid is the final output.
"""

def _get_neighbors(r, c, H, W):
    """ Get orthogonal neighbors within grid bounds. """
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < H - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < W - 1: neighbors.append((r, c + 1))
    return neighbors

def _find_largest_component(grid_np):
    """ Finds the coordinates of the largest connected component of non-background pixels. """
    H, W = grid_np.shape
    visited = set()
    largest_component_pixels = []
    max_size = 0

    for r in range(H):
        for c in range(W):
            # Check if pixel is non-background (not 0) and not yet visited
            if grid_np[r, c] != 0 and (r, c) not in visited:
                current_component_pixels = []
                q = deque([(r, c)])
                visited.add((r, c))
                
                # Start BFS to find the connected component
                while q:
                    row, col = q.popleft()
                    current_component_pixels.append((row, col))
                    
                    # Check neighbors
                    for nr, nc in _get_neighbors(row, col, H, W):
                        if grid_np[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                # Check if this component is the largest found so far
                if len(current_component_pixels) > max_size:
                    max_size = len(current_component_pixels)
                    largest_component_pixels = current_component_pixels

    return largest_component_pixels

def _get_bounding_box(pixels):
    """ Calculates the bounding box for a list of pixel coordinates. """
    if not pixels:
        return None
        
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Extracts the largest connected component of non-background pixels by finding its bounding box
    and cropping the input grid to that box.
    """
    # Convert input grid to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    H, W = grid_np.shape

    if H == 0 or W == 0:
        return [] # Handle empty input

    # Step 1 & 2: Find the largest connected component of non-background pixels
    largest_component = _find_largest_component(grid_np)

    if not largest_component:
        # Handle case where there are no non-background pixels or only background
        # Based on examples, we expect an object, but return empty grid just in case.
         # Or maybe return the original grid if that seems more appropriate?
         # Given the task, returning empty seems safer if no object is found.
         # Let's return an empty list of lists based on ARC structure.
         return []

    # Step 3: Determine the bounding box of this component
    bounding_box = _get_bounding_box(largest_component)
    if bounding_box is None:
         return [] # Should not happen if largest_component is not empty

    min_r, min_c, max_r, max_c = bounding_box
    
    # Step 4: Extract the subgrid defined by the bounding box
    output_grid_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Step 5: Convert back to list of lists format for the output
    output_grid = output_grid_np.tolist()

    return output_grid
```