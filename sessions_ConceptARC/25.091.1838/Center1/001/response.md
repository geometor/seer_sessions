```python
import numpy as np
import math
from collections import deque

"""
Identifies contiguous regions of white pixels (color 0) that are entirely enclosed 
orthogonally by pixels of a single non-white color. For each such enclosed white region, 
it calculates the geometric center based on the region's bounding box and fills 
the pixel at the center coordinates with the color of the enclosing shape.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling the center of enclosed white regions.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input grid to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    
    # Keep track of visited white pixels to avoid redundant searches
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is white (0) and hasn't been visited yet
            if grid[r, c] == 0 and not visited[r, c]:
                # Found the start of a potential enclosed white region
                region_coords = set()
                neighbor_pixels = {} # Store neighbor coords and their colors: {(nr, nc): color}
                is_enclosed = True # Assume enclosed until proven otherwise
                enclosing_color = -1 # Placeholder for the single enclosing color
                
                # Use BFS to find the connected white region and its neighbors
                queue = deque([(r, c)])
                visited[r, c] = True
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_coords.add((curr_r, curr_c))
                    
                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if neighbor is within grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_val = grid[nr, nc]
                            if neighbor_val == 0: # Neighbor is also white
                                if not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    queue.append((nr, nc))
                            else: # Neighbor is non-white (part of the potential boundary)
                                if enclosing_color == -1: # First boundary pixel found
                                     enclosing_color = neighbor_val
                                elif neighbor_val != enclosing_color: # Found a different boundary color
                                    is_enclosed = False
                                # Store neighbor info regardless for complete check later if needed, 
                                # although strict check can break early
                                neighbor_pixels[(nr, nc)] = neighbor_val
                                if not is_enclosed: # Optimization: if already not enclosed, stop checking neighbors for color consistency
                                    pass 
                        else:
                            # Touched the grid boundary, so cannot be fully enclosed
                            is_enclosed = False
                            # Can break BFS early if enclosure is the only goal, but finish finding region size for centering
                
                # After BFS, check if the region was truly enclosed by a single color
                # Re-evaluate based on all neighbors found
                final_neighbor_colors = set(neighbor_pixels.values())
                if len(final_neighbor_colors) != 1 or 0 in final_neighbor_colors:
                     is_enclosed = False

                if is_enclosed and len(region_coords) > 0:
                    # Calculate bounding box of the white region
                    min_r = min(row for row, col in region_coords)
                    max_r = max(row for row, col in region_coords)
                    min_c = min(col for row, col in region_coords)
                    max_c = max(col for row, col in region_coords)
                    
                    # Calculate the geometric center (floor division for integer coordinates)
                    center_r = (min_r + max_r) // 2
                    center_c = (min_c + max_c) // 2
                    
                    # Ensure the calculated center is actually part of the white region 
                    # (important for non-convex or oddly shaped regions)
                    # Although the current logic fills the center *coordinate*, not necessarily a pixel *within* the original white region.
                    # The examples suggest filling the *coordinate*, even if it wasn't white initially for some reason (though it should be).
                    # Let's stick to filling the center coordinate if it exists.
                    
                    # Fill the center pixel in the output grid with the enclosing color
                    # The check `if (center_r, center_c) in region_coords:` could be added for strictness,
                    # but examples imply filling the calculated center regardless.
                    if 0 <= center_r < height and 0 <= center_c < width: # Ensure center is valid coordinate
                         output_grid[center_r, center_c] = enclosing_color

    # Convert the result back to a list of lists
    return output_grid.tolist()

```