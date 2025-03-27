"""
Transforms the input grid by performing a conditional flood fill operation within contiguous regions bounded by gray (5) pixels. The fill color for each distinct region is determined by the presence and priority of marker pixels (red=2, blue=1) within that region in the input grid. Red markers have higher priority than blue markers. If a region contains neither red nor blue (only white=0), it defaults to blue. Gray boundary pixels remain unchanged.
"""

import numpy as np
from collections import deque

def find_connected_regions(grid):
    """
    Identifies contiguous regions of non-gray pixels using Breadth-First Search (BFS).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of lists, where each inner list contains the (row, col) coordinates
        of the pixels belonging to a single connected region of non-gray pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []
    gray_color = 5

    for r in range(rows):
        for c in range(cols):
            # Start a BFS if the pixel is not gray and not yet visited
            if grid[r, c] != gray_color and not visited[r, c]:
                current_region = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_region.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is valid for the region (not gray, not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != gray_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the completed region to the list of regions
                if current_region:
                    regions.append(current_region)
    return regions

def transform(input_grid):
    """
    Applies the conditional flood fill transformation based on marker priorities within regions.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid. Gray pixels will remain unchanged.
    output_grid = np.copy(input_grid)
    
    # Define marker colors and default fill color
    red_color = 2
    blue_color = 1
    # Gray color (5) is implicitly handled by find_connected_regions

    # Step 1: Identify all distinct contiguous regions of non-gray pixels.
    regions = find_connected_regions(input_grid)

    # Step 2: Process each identified region to determine and apply the fill color.
    for region_coords in regions:
        region_contains_red = False
        region_contains_blue = False

        # Step 2a: Check for the presence of marker colors (red or blue) within the current region
        # using the original input_grid values.
        for r, c in region_coords:
            pixel_value = input_grid[r, c]
            if pixel_value == red_color:
                region_contains_red = True
                break # Optimization: Red has highest priority, no need to check further.
            elif pixel_value == blue_color:
                region_contains_blue = True
                # Continue checking in case a red pixel appears later in the region list

        # Step 2b: Determine the fill color based on marker priority.
        if region_contains_red:
            fill_color = red_color # Red priority
        elif region_contains_blue:
            fill_color = blue_color # Blue secondary
        else:
            # Default case: If region contains only white (0), fill with blue.
            fill_color = blue_color 

        # Step 2c: Apply the determined fill color to all pixels within this region
        # in the output grid.
        for r, c in region_coords:
            output_grid[r, c] = fill_color

    # Step 3: Return the modified output grid.
    return output_grid