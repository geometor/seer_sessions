"""
Identifies regions of 'white' (0) pixels that meet two conditions:
1. The region does not touch the boundary of the grid.
2. All non-white pixels immediately adjacent (4-directionally) to any pixel 
   within the region are 'azure' (8).
If both conditions are met, all pixels within that 'white' region are changed 
to 'green' (3) in the output grid. All other pixels retain their original color.

The process involves iterating through each cell of the grid. If a 'white' cell 
is found that hasn't been processed yet, a Breadth-First Search (BFS) is initiated 
to find all connected 'white' cells forming a region. During the BFS, it tracks 
whether any cell in the region touches the grid boundary and collects the colors 
of all adjacent non-white neighbor cells. After the BFS for a region completes, 
it checks if the boundary was touched and if the set of non-white neighbor colors 
contains *only* 'azure'. If these conditions hold, the region's color is changed 
to 'green' in the output. A 'visited' grid ensures each 'white' cell is processed 
only once.
"""

import collections
import copy # Although not strictly needed with list comprehension for this case

# Define colors (using names for clarity in the code)
WHITE = 0
GREEN = 3
AZURE = 8

def transform(input_grid):
    """
    Transforms the input grid based on enclosed white regions bordered only by azure.

    Args:
        input_grid: A list of lists representing the input grid (integers 0-9).

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []
        
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Create a copy of the input grid to modify.
    output_grid = [row[:] for row in input_grid] 
    
    # Visited grid to keep track of processed white pixels during BFS.
    visited = [[False for _ in range(width)] for _ in range(height)]

    # Iterate through each cell (pixel) of the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell is white (0) and hasn't been visited yet
            if input_grid[r][c] == WHITE and not visited[r][c]:
                
                current_region_coords = []  # Stores coordinates (r, c) of pixels in this white region
                touches_boundary = False    # Flag: True if any pixel in the region touches the grid edge
                neighbor_colors = set()     # Stores colors of adjacent non-white pixels
                
                queue = collections.deque([(r, c)]) # Initialize queue for BFS
                visited[r][c] = True                # Mark starting cell as visited
                
                # --- Start BFS to find the connected white region and analyze its surroundings ---
                while queue:
                    curr_r, curr_c = queue.popleft()
                    
                    # Add current cell coordinates to the list for this region
                    current_region_coords.append((curr_r, curr_c))
                    
                    # Check if this white cell is on the grid boundary
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_boundary = True 
                        # Note: We continue BFS to mark all connected white cells visited,
                        # even if we already know it touches the boundary or has wrong neighbors.

                    # Explore neighbors (4 directions: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if the neighbor's coordinates are within the grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_grid[nr][nc]
                            # If the neighbor is also white and hasn't been visited yet
                            if neighbor_color == WHITE and not visited[nr][nc]:
                                visited[nr][nc] = True
                                queue.append((nr, nc))
                            # If the neighbor is NOT white
                            elif neighbor_color != WHITE:
                                # Record the color of this non-white neighbor
                                neighbor_colors.add(neighbor_color)
                        # else: Neighbor is outside the grid bounds (implicitly handled by boundary check later)
                        
                # --- End BFS for the current white region ---

                # --- Condition Check and Transformation ---
                # After exploring the entire connected white region:
                # Check if:
                # 1. The region did NOT touch the boundary
                # 2. The set of non-white neighbors contains ONLY Azure (8)
                #    (This implicitly handles the case where there are no non-white neighbors,
                #     as the set would be empty, not equal to {AZURE})
                if not touches_boundary and neighbor_colors == {AZURE}:
                    # If both conditions are met, change the color of all pixels
                    # in this region to green in the output grid.
                    for pr, pc in current_region_coords:
                        output_grid[pr][pc] = GREEN
                        
    # Return the modified grid
    return output_grid