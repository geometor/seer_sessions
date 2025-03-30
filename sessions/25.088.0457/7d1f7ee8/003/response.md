```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (color 0) within the input grid. 
For each such region, it determines the colors of all non-white pixels immediately adjacent to it. 
If a white region is fully enclosed (does not touch the grid boundary) and all its adjacent non-white pixels share the exact same color, 
then the entire white region is filled with that single adjacent color in the output grid. 
Otherwise (if the region touches the boundary, or has adjacent pixels of different non-white colors, or has no adjacent non-white pixels), 
the white region remains unchanged (color 0). All original non-white pixels are preserved in the output.
"""

def transform(input_grid):
    """
    Fills enclosed white regions with the color of their single immediate surrounding frame.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    H, W = input_grid_np.shape
    output_grid_np = np.copy(input_grid_np)
    visited = np.full((H, W), False, dtype=bool)

    # Helper function to check grid bounds
    def is_valid(r, c):
        return 0 <= r < H and 0 <= c < W

    # Iterate through each cell to find starting points of white regions
    for r in range(H):
        for c in range(W):
            # If it's a white pixel and hasn't been visited yet (part of a new region)
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                
                # Initialize BFS for this white region
                region_coords = []
                adjacent_colors = set()
                touches_boundary = False
                queue = deque([(r, c)])
                visited[r, c] = True
                
                # Perform BFS to find all connected white pixels and their adjacent non-white neighbors
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_coords.append((curr_r, curr_c))

                    # Check all 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is out of bounds
                        if not is_valid(nr, nc):
                            touches_boundary = True
                            continue # Move to the next neighbor

                        # Neighbor is within bounds
                        neighbor_color = input_grid_np[nr, nc]

                        # If neighbor is white and not visited, add to queue
                        if neighbor_color == 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
                        # If neighbor is not white (part of a potential frame)
                        elif neighbor_color != 0:
                            adjacent_colors.add(neighbor_color)

                # After exploring the entire white region, check fill conditions
                # Condition: Region must NOT touch the boundary AND must have exactly ONE adjacent color
                if not touches_boundary and len(adjacent_colors) == 1:
                    fill_color = adjacent_colors.pop() # Get the single adjacent color
                    # Fill the region in the output grid
                    for fill_r, fill_c in region_coords:
                        output_grid_np[fill_r, fill_c] = fill_color
                        
    return output_grid_np.tolist()
```