import numpy as np
from collections import deque

"""
Transforms the input grid by identifying connected regions of non-green pixels. 
If a region is not adjacent to any border of the grid, it is considered 'enclosed' 
and filled with azure (color 8). Green pixels (color 3) act as barriers and 
remain unchanged.

1.  Define Barriers: Green pixels (color 3) are barriers and remain unchanged.
2.  Identify Connected Components: Find contiguous regions of non-green pixels 
    using 4-way adjacency (up, down, left, right).
3.  Check Border Adjacency: For each non-green component, determine if any pixel 
    within it lies on the grid's outer border (first/last row or first/last column).
4.  Fill Enclosed Regions: If a non-green component does *not* touch the border, 
    change the color of all pixels within that component to azure (8).
5.  Construct Output: Create the output grid where:
    - Green (3) pixels keep their color.
    - Non-green pixels in border-adjacent regions keep their original color.
    - Non-green pixels in non-border-adjacent (enclosed) regions are changed to azure (8).
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to a NumPy array for easier manipulation and access to shape
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize the output grid as a copy of the input grid.
    # Pixels will be overwritten only if they are in an enclosed region.
    output_grid = grid.copy()

    # Define barrier color and the color to fill enclosed areas
    barrier_color = 3
    fill_color = 8

    # Keep track of visited cells during component finding to avoid redundant searches
    visited = np.zeros_like(grid, dtype=bool)

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell is non-barrier and hasn't been visited as part of a component yet
            if grid[r, c] != barrier_color and not visited[r, c]:
                # Found the start of a potential new non-barrier component
                component_coords = set()
                touches_border = False
                queue = deque([(r, c)])
                visited[r, c] = True # Mark the starting cell as visited

                # Perform BFS to find the entire connected component
                while queue:
                    curr_r, curr_c = queue.popleft()
                    component_coords.add((curr_r, curr_c))

                    # Check if the current cell is on the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor is part of the component (not a barrier) 
                            # and has not been visited yet
                            if grid[nr, nc] != barrier_color and not visited[nr, nc]:
                                # Mark as visited and add to the queue to explore
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                
                # After exploring the entire component, check if it touched the border
                if not touches_border:
                    # If the component did not touch the border, fill it with the fill_color
                    for comp_r, comp_c in component_coords:
                        output_grid[comp_r, comp_c] = fill_color
                # Else (component touched the border), do nothing, pixels keep original color (already copied)

    # Convert the result back to a standard list of lists format
    return output_grid.tolist()