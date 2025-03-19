"""
1.  **Identify the Azure Object:** Locate the contiguous region of azure (8) pixels within the input grid. If no azure object is found, return the original grid unchanged.

2.  **Define Search Area:** Consider the bounding box of the azure object. Extend this bounding box by one pixel in all directions (up, down, left, and right) to create a "search area."

3.  **Iterate and Check for Enclosure:** Iterate through all pixels within the "search area". For each pixel:

    *   If the pixel is *not* azure, check if it is part of a region that is *completely enclosed* by azure pixels. A region is considered enclosed if, starting from any pixel within that region, you cannot reach the edge of the *entire grid* without crossing an azure pixel.
    *   If a pixel is part of an enclosed region, change all pixels in the enclosed region to red (2).

4.  **Output:** Return the modified grid, where all regions enclosed by azure within the search area are filled with red.
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

def is_enclosed(grid, row, col, enclosing_color):
    # Check if a pixel is enclosed by the object color using flood fill
    rows, cols = grid.shape
    if grid[row, col] == enclosing_color:
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

        if grid[r, c] == enclosing_color:
            continue
        
        # Add neighbors to the queue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            queue.append((r + dr, c + dc))
    return True

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Fills a connected region of target_color with replacement_color.
    """
    rows, cols = grid.shape
    if not (0 <= row < rows and 0 <= col < cols):
        return  # Out of bounds

    if grid[row, col] != target_color:
        return  # Not the target color

    grid[row, col] = replacement_color
    
    # Recursively fill adjacent pixels
    flood_fill(grid, row + 1, col, target_color, replacement_color)
    flood_fill(grid, row - 1, col, target_color, replacement_color)
    flood_fill(grid, row, col + 1, target_color, replacement_color)
    flood_fill(grid, row, col - 1, target_color, replacement_color)


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure object.
    azure_object_bounds = find_object(input_grid, 8)
    if azure_object_bounds is None:
        return output_grid # Nothing to do if no azure

    (min_row, min_col), (max_row, max_col) = azure_object_bounds

     # Iterate through the grid, focusing on the search area.
    for r in range(min_row-1, max_row + 2):  # Search area around azure.
        for c in range(min_col -1, max_col + 2):
            if 0 <= r < input_grid.shape[0] and 0 <= c < input_grid.shape[1]:
                if input_grid[r,c] != 8: #if the pixel not azure
                    if is_enclosed(input_grid, r, c, 8):
                        # Fill the entire enclosed region with red.
                        flood_fill(output_grid, r, c, input_grid[r,c], 2)

    return output_grid