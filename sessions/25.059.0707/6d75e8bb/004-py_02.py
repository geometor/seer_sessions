"""
1.  **Identify the Azure Shape:** Find the contiguous block of azure (8) pixels within the input grid.
2.  **Locate Internal 'Holes':** Within the azure shape, identify any "holes" or enclosed regions. These are areas of white pixels (0) that are completely surrounded by the azure shape.
3. **Fill the Holes:** If a region defined in step 2 is present in the azure object, change color of the region to the right and below any azure pixel adjacent to those regions to red(2).
4.  **Output:** Produce the modified grid where the enclosed region within the azure shape is now colored red (2). The description indicates the pixels that change from the background color to red are bounded to pixels adjacent to the identified azure object.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle cases where the color is not found.

    #find top-left and bottom-right points of the object
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)

    return (min_row, min_col), (max_row, max_col)

def is_enclosed(grid, row, col, object_color):
    # Check if a pixel is enclosed by the object color using flood fill
    rows, cols = grid.shape
    if grid[row, col] == object_color:
        return False

    visited = set()
    queue = [(row, col)]
    
    while queue:
        r, c = queue.pop(0)

        if (r,c) in visited:
            continue
        visited.add((r,c))
        
        if not (0 <= r < rows and 0 <= c < cols):
            return False # Reached the edge, so not enclosed

        if grid[r, c] == object_color:
            continue
        
        # Add neighbors to the queue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            queue.append((r + dr, c + dc))
    return True


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure object.
    azure_object_bounds = find_object(input_grid, 8)
    if azure_object_bounds is None:
        return output_grid # Nothing to do if no azure

    (min_row, min_col), (max_row, max_col) = azure_object_bounds

     # Iterate through the grid, focusing near the azure object to find holes.
    for r in range(min_row-1, max_row + 2):  # Check range around the azure shape to detect holes.
        for c in range(min_col -1, max_col + 2):
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]: # Check grid limits.
                if is_enclosed(input_grid, r, c, 8):
                    #fill to the right and below
                    if r+1 <= max_row and input_grid[r+1, c] == 8:
                        output_grid[r+1,c] = 2
                    if c+1 <= max_col and input_grid[r,c+1] == 8:
                        output_grid[r,c+1] = 2

    return output_grid