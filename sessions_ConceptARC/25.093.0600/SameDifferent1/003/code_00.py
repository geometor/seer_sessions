import numpy as np
from collections import deque

"""
Identifies connected regions of non-zero colors in the input grid using 4-way 
adjacency (up, down, left, right). If any cell belonging to a specific region 
is located on the grid's outermost border (top row, bottom row, leftmost 
column, or rightmost column), then the entire region is removed (replaced 
with the background color '0'). Regions that are entirely contained within the 
grid and do not touch any border are preserved in the output grid.
"""

def _find_regions_and_filter(grid_np):
    """
    Finds all connected regions of non-zero cells using BFS and determines
    if they touch the border. Returns only the regions that do NOT touch
    the border.

    Args:
        grid_np (np.array): The input grid as a NumPy array.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              to keep and contains 'color' and 'cells' (a list of 
              (row, col) tuples).
    """
    rows, cols = grid_np.shape
    visited = set()
    regions_to_keep = []

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and hasn't been visited yet, it's the start of a new potential region
            if grid_np[r, c] != 0 and (r, c) not in visited:
                color = grid_np[r, c]
                current_region_cells = []
                touches_border = False
                q = deque([(r, c)])
                visited.add((r, c))
                
                # Perform Breadth-First Search (BFS) to find all connected cells of the same color
                while q:
                    row, col = q.popleft()
                    current_region_cells.append((row, col))

                    # Check if the current cell is on the border
                    # Use >= rows - 1 and >= cols - 1 for safety, although == should suffice
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        touches_border = True # Mark the entire region as touching the border

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color and hasn't been visited
                            if grid_np[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                # After exploring the entire region, decide whether to keep it
                if not touches_border:
                    regions_to_keep.append({
                        'color': color,
                        'cells': current_region_cells,
                    })
                    
    return regions_to_keep

def transform(input_grid):
    """
    Transforms the input grid by removing connected regions of non-zero colors
    if they touch the grid border.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid with the same dimensions, filled with the background color (0)
    output_grid = np.zeros_like(grid_np)

    # Find all regions in the input grid that do NOT touch the border
    regions_to_keep = _find_regions_and_filter(grid_np)

    # Iterate through the regions that should be kept
    for region in regions_to_keep:
        color = region['color']
        # Place the color of the kept region onto the corresponding cells in the output grid
        for r, c in region['cells']:
            output_grid[r, c] = color

    # Convert the resulting NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()