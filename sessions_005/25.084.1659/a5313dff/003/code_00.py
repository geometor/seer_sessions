import numpy as np
from collections import deque

"""
Identifies enclosed regions ('holes') surrounded by red (2) pixels. 
An enclosed region consists of all connected pixels (including any color) 
that cannot reach the grid border via a path of non-red pixels.
If an enclosed region contains at least one red (2) pixel within its area 
in the input grid, all white (0) pixels within that specific region are 
changed to blue (1) in the output grid. 
Pixels outside enclosed regions, red pixels, and pixels in enclosed regions 
that do not contain any red pixels remain unchanged. Non-white pixels 
within enclosed regions that *do* contain red pixels also remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white areas with blue if 
    the area contains any red pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)
    
    # 1. Identify external area: pixels reachable from the border via non-red paths
    is_external = np.zeros_like(input_grid, dtype=bool)
    q = deque()
    
    # Initialize queue with non-red border pixels
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid[r, c] != 2 and not is_external[r, c]:
                is_external[r, c] = True
                q.append((r, c))
    for c in range(width):
        for r in [0, height - 1]:
            if input_grid[r, c] != 2 and not is_external[r, c]:
                is_external[r, c] = True
                q.append((r, c))

    # Perform BFS for external area
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if input_grid[nr, nc] != 2 and not is_external[nr, nc]:
                    is_external[nr, nc] = True
                    q.append((nr, nc))

    # 2. Identify enclosed regions and process them
    visited_enclosed = np.zeros_like(input_grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            # If pixel is not external and not yet visited as part of an enclosed region
            if not is_external[r, c] and not visited_enclosed[r, c]:
                # Start BFS to find this enclosed region
                current_region_pixels = []
                contains_red = False
                region_q = deque([(r, c)])
                visited_enclosed[r, c] = True
                
                while region_q:
                    curr_r, curr_c = region_q.popleft()
                    current_region_pixels.append((curr_r, curr_c))
                    
                    # Check if this pixel is red in the original grid
                    if input_grid[curr_r, curr_c] == 2:
                        contains_red = True
                        
                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < height and 0 <= nc < width:
                            # Add neighbor if it's part of the same enclosed area 
                            # (i.e., not external) and not yet visited
                            if not is_external[nr, nc] and not visited_enclosed[nr, nc]:
                                visited_enclosed[nr, nc] = True
                                region_q.append((nr, nc))
                                
                # 3. Process the found enclosed region
                # If the region contained at least one red pixel
                if contains_red:
                    # Change all original white pixels in this region to blue
                    for pix_r, pix_c in current_region_pixels:
                        if input_grid[pix_r, pix_c] == 0:
                            output_grid[pix_r, pix_c] = 1
                            
    return output_grid
