"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels. A contiguous region is a group of azure pixels connected horizontally or vertically.
2.  **Check for White Pixel Above:** For each azure region, check if *any* pixel within the region has a white (0) pixel directly above it.
3.  **Transform if Condition Met:** If any pixel within an azure region has a white pixel directly above it, change *all* pixels in that azure region to blue (1).
4.  **Otherwise No Change:** If the condition in step 3 is not met, the azure region remains unchanged.
"""

import numpy as np

def get_contiguous_region(input_grid, start_r, start_c, visited, target_color):
    """
    Finds a contiguous region of a specified color using Depth-First Search.
    """
    rows, cols = input_grid.shape
    region = []
    stack = [(start_r, start_c)]

    while stack:
        r, c = stack.pop()

        if (r < 0 or r >= rows or c < 0 or c >= cols or
            visited[r, c] or input_grid[r, c] != target_color):
            continue

        visited[r, c] = True
        region.append((r, c))

        stack.append((r + 1, c))
        stack.append((r - 1, c))
        stack.append((r, c + 1))
        stack.append((r, c - 1))
    return region

def transform(input_grid):
    """
    Transforms the input grid based on the presence of white pixels above azure regions.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is azure and not visited
            if input_grid[r, c] == 8 and not visited[r, c]:
                # Find the contiguous azure region
                azure_region = get_contiguous_region(input_grid, r, c, visited, 8)

                # Check for white pixel above any pixel in the region
                region_changed = False
                for row, col in azure_region:
                    if row > 0 and input_grid[row - 1, col] == 0:
                        region_changed = True
                        break  # No need to check further if one is found

                # Change entire region to blue if condition is met
                if region_changed:
                    for row, col in azure_region:
                        output_grid[row, col] = 1

    return output_grid