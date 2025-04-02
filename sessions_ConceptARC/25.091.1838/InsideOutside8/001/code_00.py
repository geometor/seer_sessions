import numpy as np
from collections import deque, Counter

"""
Keep only the target-colored pixels that are located inside the region defined 
by the boundary-colored shape. Replace everything else, including the boundary 
shape itself, with the background color (0).

The 'inside' region is determined by performing a flood fill starting from the 
background pixels (0) on the grid's border. Pixels reachable by this flood fill 
without crossing the boundary color are considered 'outside'. Target-colored 
pixels not marked as 'outside' are considered 'inside' and are kept in the 
output grid. The boundary color is identified as the non-background color with 
the highest pixel count in the input grid. All other non-background colors are 
considered target colors.
"""

def find_colors(input_grid_np):
    """Identifies background, boundary, and target colors."""
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    if not non_background_colors:
        # Only background color present
        return background_color, boundary_color, target_colors
        
    # Heuristic: Boundary color is the non-background color with the most pixels
    boundary_color = max(non_background_colors, key=non_background_colors.get)
    
    # All other non-background colors are targets
    target_colors = set(non_background_colors.keys()) - {boundary_color}
    
    return background_color, boundary_color, target_colors

def transform(input_grid):
    """
    Transforms the input grid based on the containment rule.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # Initialize output grid with background color
    background_color = 0
    output_grid_np = np.full_like(input_grid_np, background_color)
    
    # Identify the boundary and target colors
    _, boundary_color, target_colors = find_colors(input_grid_np)

    # If there's no boundary or no targets, return the background grid
    if boundary_color is None or not target_colors:
         return output_grid_np.tolist()

    # Determine the 'outside' region using flood fill from borders
    visited = np.zeros_like(input_grid_np, dtype=bool)
    q = deque()

    # Add border pixels that are NOT the boundary color to the queue
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] != boundary_color and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # Avoid double-adding corners
        for r in [0, height - 1]:
             if input_grid_np[r, c] != boundary_color and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))

    # Perform flood fill (Breadth-First Search)
    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If neighbor is not boundary color and not visited
                if input_grid_np[nr, nc] != boundary_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Populate the output grid
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            # If the pixel has a target color AND it was NOT visited by the flood fill (i.e., it's 'inside')
            if pixel_color in target_colors and not visited[r, c]:
                # Keep this pixel in the output grid
                output_grid_np[r, c] = pixel_color
                
    # Convert back to list of lists and return
    return output_grid_np.tolist()