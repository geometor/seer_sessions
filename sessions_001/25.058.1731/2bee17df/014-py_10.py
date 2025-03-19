"""
1.  **Identify White Regions:** Find all contiguous regions of white (0) pixels in the input grid.
2.  **Check for Enclosure:** For each white region, determine if it is *enclosed*. A region is considered enclosed if it is completely surrounded by non-white pixels of any color, such that no white pixel in the region can reach the edge of the grid without crossing a non-white pixel.
3.  **Replace Enclosed Regions:** If a white region is enclosed, change all pixels within that region to green (3).
4. **Preserve Other Pixels**: All other pixels not part of an enclosed white region retain their original colors.
"""

import numpy as np

def get_contiguous_regions(grid, color):
    """
    Finds all contiguous regions of a specific color in the grid.
    Returns a list of sets, where each set contains the (row, col) coordinates of a contiguous region.
    """
    visited = set()
    regions = []

    def dfs(row, col, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] != color
            or (row, col) in visited
        ):
            return
        visited.add((row, col))
        current_region.add((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = set()
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_enclosed(grid, region):
    """
    Checks if a region is enclosed (cannot reach the edge via flood fill).
    """
    if not region:
        return False

    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Create a slightly larger grid for flood fill
    flood_grid = np.copy(grid)

    # Mark region in flood_grid as -1 to avoid re-visiting it
    for r,c in region:
        flood_grid[r,c] = -1
        

    # Use a stack for iterative DFS (flood fill)
    stack = []

    # Add border pixels of bounding rect to stack,
    #   only if within original image
    for c in range(min_col, max_col + 1):
        if min_row > 0:
            stack.append( (min_row-1, c) )
        if max_row < grid.shape[0] -1:
            stack.append( (max_row+1, c) )

    for r in range(min_row, max_row+1):
        if min_col > 0:
            stack.append( (r, min_col-1) )
        if max_col < grid.shape[1]-1:
            stack.append( (r, max_col+1) )

    # Perform flood fill from the added border pixels
    visited = set()
    while stack:
        row, col = stack.pop()

        if (row,col) in visited:
            continue
        visited.add((row,col))

        # Check if out-of-bounds in original grid
        if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]:
            continue

        # Check if we hit a 'white' pixel (marked as -1 for now in flood_grid)
        # if we hit original region, it is not enclosed
        if flood_grid[row,col] == -1:
          continue

        # If not an enclosing color, push neighbours to stack
        if flood_grid[row, col] == 0:
            stack.append((row + 1, col))
            stack.append((row - 1, col))
            stack.append((row, col + 1))
            stack.append((row, col - 1))

    # Check if any of the original pixels were re-visited during flood fill
    # if any were, they are not enclosed
    for r,c in region:
        if (r,c) not in visited:
            return True
    return False
    
def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find all contiguous regions of white pixels
    white_regions = get_contiguous_regions(input_grid, 0)

    # Iterate through each white region
    for region in white_regions:
        # Check if the region is enclosed
        if is_enclosed(input_grid, region):
            # Change all pixels in the region to green
            for row, col in region:
                output_grid[row, col] = 3

    return output_grid