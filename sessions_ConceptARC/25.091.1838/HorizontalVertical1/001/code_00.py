import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) that are not connected to the grid border (internal regions).
For each such internal region, it checks if it is bounded by a single, uniform non-white color.
If it is, it determines if the region is partially enclosed (connected to the border white region via adjacency, C-like) or fully enclosed (O-like).
Based on the boundary color and enclosure type, it fills the internal region with a new color:
- Partially enclosed (C-like): Fill with Green (3).
- Fully enclosed (O-like):
    - Boundary Red (2) or Yellow (4): Fill with Orange (7).
    - Boundary Orange (7): Fill with Green (3).
The original non-white shapes and the background white region remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Keep track of visited pixels during flood fills
    visited = np.zeros_like(input_grid, dtype=bool)
    # Keep track of pixels belonging to the background white region
    is_background = np.zeros_like(input_grid, dtype=bool)

    q = deque()

    # 1. Identify the background white region (connected to borders) using BFS
    for r in range(height):
        for c in [0, width - 1]: # Left and right borders
            if input_grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                is_background[r, c] = True
                q.append((r, c))
    for c in range(width):
        for r in [0, height - 1]: # Top and bottom borders
             if input_grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                is_background[r, c] = True
                q.append((r, c))

    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-directional neighbors
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                is_background[nr, nc] = True
                q.append((nr, nc))

    # 2. Iterate through the grid to find internal white regions
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited (i.e., not background)
            if input_grid[r, c] == 0 and not visited[r, c]:
                
                # Start a BFS for this potential internal region
                internal_q = deque([(r, c)])
                visited[r, c] = True
                current_region_pixels = [(r, c)]
                boundary_neighbors = set() # Store (nr, nc, color) tuples
                is_partially_enclosed = False 

                while internal_q:
                    curr_r, curr_c = internal_q.popleft()

                    # Check neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_grid[nr, nc]
                            
                            if neighbor_color == 0:
                                # Check if adjacent to known background
                                if is_background[nr, nc]:
                                    is_partially_enclosed = True
                                
                                # If this white neighbor hasn't been visited, add to queue
                                if not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    internal_q.append((nr, nc))
                                    current_region_pixels.append((nr, nc))
                            else:
                                # It's a non-white boundary neighbor
                                boundary_neighbors.add((nr, nc, neighbor_color))
                        # else: neighbor is out of bounds, implicitly connected to 'outside'
                        # This doesn't directly make it partially enclosed by our definition,
                        # which relies on connection to the *white* background region.
                        
                # 3. Analyze the found region
                boundary_colors = set(color for _, _, color in boundary_neighbors)

                # Check if bounded by a single color
                if len(boundary_colors) == 1:
                    boundary_color = list(boundary_colors)[0]
                    fill_color = -1 # Use -1 to indicate no fill initially

                    # Determine fill color based on rules
                    if is_partially_enclosed:
                        # C-like shape rule
                        fill_color = 3 # Green
                    else:
                        # O-like shape rule
                        if boundary_color == 2 or boundary_color == 4: # Red or Yellow
                            fill_color = 7 # Orange
                        elif boundary_color == 7: # Orange
                            fill_color = 3 # Green
                            
                    # 4. Apply fill if a color was determined
                    if fill_color != -1:
                        for pr, pc in current_region_pixels:
                            output_grid[pr, pc] = fill_color

    return output_grid