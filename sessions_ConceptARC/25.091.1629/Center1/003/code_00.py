import numpy as np
from collections import deque

"""
Identifies enclosed white regions (color 0) within a grid that are surrounded by a single non-white color. 
For each such enclosed region, the pixel at the geometric center of the region's bounding box 
is changed from white to the color of the enclosing shape.
"""

def get_neighbors(r, c):
    """ Generate 8 neighbor coordinates for a coordinate (r, c). """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            neighbors.append((r + dr, c + dc))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid by filling the center of enclosed white regions.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    H, W = input_grid_np.shape
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # Iterate through each cell to find starting points for white regions
    for r in range(H):
        for c in range(W):
            # If it's a white cell (0) and not yet visited as part of a region
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                
                # Start a Breadth-First Search (BFS) to find the connected white region
                q = deque([(r, c)])
                region_coords = set()
                boundary_colors = set()
                touches_edge = False
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                # Keep track of nodes added to the queue to prevent duplicates
                queued = set([(r,c)]) 

                # Process the queue for the current region
                while q:
                    curr_r, curr_c = q.popleft()

                    # Skip if already visited (should not happen with 'queued' set but good practice)
                    if visited[curr_r, curr_c]:
                        continue
                        
                    # Mark current cell as visited and add to region
                    visited[curr_r, curr_c] = True
                    region_coords.add((curr_r, curr_c))

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check 8 neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c):
                        # Check if neighbor is out of bounds
                        if not (0 <= nr < H and 0 <= nc < W):
                            touches_edge = True
                            continue # Don't process out-of-bounds neighbors further

                        neighbor_color = input_grid_np[nr, nc]

                        # If neighbor is white and not visited or queued, add to queue
                        if neighbor_color == 0:
                            if not visited[nr, nc] and (nr, nc) not in queued:
                                q.append((nr, nc))
                                queued.add((nr,nc))
                        # If neighbor is non-white, record its color as a boundary color
                        else:
                            boundary_colors.add(neighbor_color)
                
                # After exploring the whole region, check if it's enclosed
                # Must not touch edge and must be surrounded by exactly one non-white color
                if not touches_edge and len(boundary_colors) == 1:
                    enclosing_color = list(boundary_colors)[0] # Get the single enclosing color
                    
                    # Calculate center coordinates using integer division (floor)
                    center_r = min_r + (max_r - min_r) // 2
                    center_c = min_c + (max_c - min_c) // 2

                    # Check if the calculated center is actually part of the white region found
                    # This ensures we only color pixels that were originally white and part of this specific region.
                    if (center_r, center_c) in region_coords:
                        # Modify the output grid at the center pixel
                        output_grid[center_r, center_c] = enclosing_color

    # Convert back to list of lists before returning
    return output_grid.tolist()