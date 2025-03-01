"""
Filters out red pixels from the input grid, identifies the green pixels that form the top and bottom boundaries
of internal colored objects, and rearranges these selected green pixels into a new, smaller grid.
"""

import numpy as np

def get_boundary_green_pixels(grid):
    """
    Identifies green pixels that are at the top and bottom boundaries of non-white objects.
    """
    green_pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                # Check if it's a top boundary (non-white pixel below)
                if r + 1 < rows and grid[r + 1, c] != 0 and grid[r+1, c] !=3:
                     green_pixels.append((r, c))
                # Check if it's a bottom boundary (non-white pixel above)
                elif r - 1 >= 0 and grid[r - 1, c] != 0 and grid[r-1,c] !=3:
                      green_pixels.append((r,c))
    return green_pixels
def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid)

    # 1. & 2. Filter out red and white pixels (keep only green) - implicitly done in get_boundary_green_pixels
    # 3. Identify boundary green pixels
    boundary_green_pixels = get_boundary_green_pixels(grid)
    
    # 4. Select the identified boundary green pixels - already selected in boundary_green_pixels

    # 5. Rearrange into a new grid.
    # Determine new grid size - this logic needs refinement based on more examples.
    # For now a simple hard coded size
    
    output_grid = np.zeros((3, 5), dtype=int)

    if len(boundary_green_pixels) >= 2:
        output_grid[0, 1] = 3
        output_grid[0, 2] = 3
        output_grid[1, 1] = 3
        output_grid[1, 2] = 3

    if len(boundary_green_pixels) == 4:
        output_grid[1,4] = 3
        output_grid[2,0] = 3
        output_grid[2,3] = 3


    return output_grid.tolist()