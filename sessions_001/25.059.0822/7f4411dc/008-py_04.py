"""
1. Find Contiguous Regions: Identify all contiguous regions of pixels that have the same color (excluding white).  A contiguous region is a group of pixels where each pixel is directly adjacent (up, down, left, or right, but not diagonally) to at least one other pixel in the same region.

2. Check for White Neighbors: For each identified region, determine if ANY pixel within that region is immediately adjacent (including diagonally) to a white pixel (value 0).

3.  Conditional Removal Based on Group Size: If a region has at least one pixel adjacent to white, and the maximum contiguous length within the region, in any direction is three or greater, change all pixels in that region to white (0).  Otherwise, leave the region unchanged.

"""

import numpy as np

def is_adjacent_to_white(grid, r, c):
    """Checks if a cell at (r, c) is adjacent to a white (0) cell."""
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                return True
    return False

def get_contiguous_group_size(grid, r, c, color):
    """
    Calculate maximum group size of contiguous cells of same color in any single direction.
    """
    rows, cols = grid.shape
    max_size = 0

    # Check Horizontal
    count = 0
    for dc in range(-cols + 1, cols):
        nc = c + dc
        if 0 <= nc < cols and grid[r,nc] == color:
            count += 1
        elif count > 0:
            max_size = max(count,max_size)
            count = 0

    #Check Vertical
    count = 0
    for dr in range(-rows + 1, rows):
        nr = r + dr
        if 0 <= nr < rows and grid[nr,c] == color:
            count += 1
        elif count > 0:
            max_size = max(count,max_size)
            count = 0
    
    # Check diagonals
    for slope in [-1,1]:
        count = 0
        for dd in range(-max(rows,cols)+1,max(rows,cols)):
            nr = r + dd
            nc = c + slope*dd

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr,nc] == color:
                count +=1
            elif count > 0:
                max_size = max(count,max_size)
                count = 0            
    
    return max_size

def get_contiguous_regions(grid):
    """Identifies all contiguous regions of non-white pixels."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(r, c, color, current_region):
        """Depth-first search to find all pixels in a contiguous region."""
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_region.append((r, c))
        # Check adjacent cells (not diagonally)
        dfs(r + 1, c, color, current_region)
        dfs(r - 1, c, color, current_region)
        dfs(r, c + 1, color, current_region)
        dfs(r, c - 1, color, current_region)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                current_region = []
                dfs(r, c, grid[r, c], current_region)
                regions.append((grid[r,c], current_region))  # Store color and region
    return regions

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    regions = get_contiguous_regions(input_grid)

    for color, region in regions:
        adjacent_to_white = False
        max_size = 0
        for r, c in region:
            if is_adjacent_to_white(input_grid, r, c):
                adjacent_to_white = True
            max_size = max(max_size,get_contiguous_group_size(input_grid,r,c,color))

        if adjacent_to_white and max_size >=3:
            for r, c in region:
                output_grid[r, c] = 0  # Change to white

    return output_grid