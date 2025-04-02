```python
import numpy as np
from collections import deque

"""
Keep only the target-colored pixels that are located 'inside' the region 
defined by the boundary-colored shape. Replace everything else, including 
the boundary shape itself, with the background color (0).

The boundary color is identified as the non-background color (non-0) with the 
highest pixel count. Target colors are all other non-background colors.

The 'outside' region is determined by performing a flood fill (BFS) starting 
from all border pixels that are *not* the boundary color. This fill propagates 
through adjacent cells (up, down, left, right) but cannot cross the boundary 
color. Pixels reached by this fill are marked as 'outside'. 

Target-colored pixels in the input grid that were *not* marked as 'outside' 
are considered 'inside' and are placed onto the output grid at their 
corresponding positions. The rest of the output grid remains the background color.
"""

def find_colors(input_grid_np):
    """
    Identifies background (0), boundary (most frequent non-0), and target 
    (other non-0) colors based on pixel counts.

    Args:
        input_grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        tuple: (background_color, boundary_color, target_colors)
               boundary_color is None if only background exists or only one non-bg color.
               target_colors is an empty set if no targets exist.
    """
    unique_colors, counts = np.unique(input_grid_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    
    background_color = 0
    # Dictionary of non-background colors and their counts
    non_background_colors = {c: count for c, count in color_counts.items() if c != background_color}
    
    boundary_color = None
    target_colors = set()
    
    # If there are non-background colors present
    if non_background_colors:
        # Boundary color is the most frequent non-background color
        boundary_color = max(non_background_colors, key=non_background_colors.get)
        # Target colors are all other non-background colors
        target_colors = set(non_background_colors.keys()) - {boundary_color}
        # If only one non-background color exists, it's the boundary, and targets are empty
        # No need for explicit check, the set difference handles this.
        
    return background_color, boundary_color, target_colors


def transform(input_grid):
    """
    Transforms the input grid based on the containment rule using flood fill.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    # --- 1. Identify Colors ---
    background_color, boundary_color, target_colors = find_colors(input_grid_np)

    # Initialize the output grid with the background color
    output_grid_np = np.full_like(input_grid_np, background_color)

    # --- Handle Edge Cases ---
    # If no boundary is found (e.g., only background color) or no target colors exist,
    # the output will be just the background grid.
    if boundary_color is None or not target_colors:
         return output_grid_np.tolist()

    # --- 2. Determine the 'Outside' Region using Flood Fill (BFS) ---
    # is_outside grid keeps track of pixels reachable from the border without crossing the boundary
    is_outside = np.zeros_like(input_grid_np, dtype=bool)
    q = deque()

    # Initialize queue with border pixels that are NOT the boundary color
    for r in range(height):
        for c in [0, width - 1]: # First and last columns
            if input_grid_np[r, c] != boundary_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # First and last rows (excluding corners already checked)
        for r in [0, height - 1]:
             if input_grid_np[r, c] != boundary_color and not is_outside[r, c]:
                is_outside[r, c] = True
                q.append((r, c))

    # Perform flood fill (Breadth-First Search)
    while q:
        r, c = q.popleft()
        
        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is NOT boundary color AND NOT already marked as outside
                if input_grid_np[nr, nc] != boundary_color and not is_outside[nr, nc]:
                    is_outside[nr, nc] = True # Mark as outside
                    q.append((nr, nc)) # Add to queue for further exploration

    # --- 3. Populate the Output Grid ---
    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]
            # If the pixel has a target color AND it was NOT marked as outside (i.e., it's 'inside')
            if pixel_color in target_colors and not is_outside[r, c]:
                # Keep this pixel in the output grid
                output_grid_np[r, c] = pixel_color
                
    # Convert the final NumPy array back to a list of lists and return
    return output_grid_np.tolist()
```