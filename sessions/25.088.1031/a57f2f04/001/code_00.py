import numpy as np
from collections import deque

"""
The transformation identifies distinct regions enclosed by an azure (8) border. 
Within each region, it finds the smallest rectangular bounding box containing all non-white (0) and non-azure (8) pixels. This bounding box defines a "pattern kernel".
The transformation then tiles this pattern kernel across the entire corresponding enclosed region in the output grid, starting from the region's top-left corner. 
The azure border remains unchanged.
"""

def find_connected_region(grid, start_r, start_c, background_color, visited):
    """Finds all connected pixels of non-background color using BFS."""
    height, width = grid.shape
    if not (0 <= start_r < height and 0 <= start_c < width) or \
       visited[start_r, start_c] or \
       grid[start_r, start_c] == background_color:
        return []

    queue = deque([(start_r, start_c)])
    region_coords = set()
    visited[start_r, start_c] = True

    while queue:
        r, c = queue.popleft()
        region_coords.add((r, c))

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               not visited[nr, nc] and \
               grid[nr, nc] != background_color:
                visited[nr, nc] = True
                queue.append((nr, nc))

    return list(region_coords)

def transform(input_grid):
    """
    Tiles a pattern derived from non-white pixels within bordered regions across those regions.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 8
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each cell to find starting points of regions
    for r in range(height):
        for c in range(width):
            # If the cell is not background and not yet visited, it's part of a new region
            if input_grid[r, c] != background_color and not visited[r, c]:
                # Find all connected pixels in this region
                region_pixels = find_connected_region(input_grid, r, c, background_color, visited)

                if not region_pixels:
                    continue # Should not happen if the initial check passed, but good practice

                # Identify the "seed" pixels (non-white, non-background) within the region
                seed_pixels = [(pr, pc) for pr, pc in region_pixels if input_grid[pr, pc] != 0]

                # If there are no seed pixels (region is all white), leave it as is
                if not seed_pixels:
                    # Mark all pixels in this white region as visited to avoid redundant checks
                    for pr, pc in region_pixels:
                         visited[pr,pc] = True # Make sure find_connected_region handles visited correctly
                    continue # Skip tiling for all-white regions

                # Determine the bounding box of the seed pixels to define the kernel area
                min_r_kernel = min(pr for pr, pc in seed_pixels)
                max_r_kernel = max(pr for pr, pc in seed_pixels)
                min_c_kernel = min(pc for pr, pc in seed_pixels)
                max_c_kernel = max(pc for pr, pc in seed_pixels)

                # Calculate kernel dimensions
                kernel_h = max_r_kernel - min_r_kernel + 1
                kernel_w = max_c_kernel - min_c_kernel + 1

                # Extract the kernel pattern from the input grid
                kernel = input_grid[min_r_kernel : max_r_kernel + 1, min_c_kernel : max_c_kernel + 1]

                # Determine the top-left corner of the entire region (not just the kernel)
                # This serves as the reference point for tiling calculation
                region_min_r = min(pr for pr, pc in region_pixels)
                region_min_c = min(pc for pr, pc in region_pixels)

                # Iterate through all pixels in the identified region and apply the kernel pattern
                for pr, pc in region_pixels:
                    # Calculate the corresponding position within the kernel using modulo arithmetic
                    # Relative position within the region determines the kernel index
                    kernel_row_index = (pr - region_min_r) % kernel_h
                    kernel_col_index = (pc - region_min_c) % kernel_w

                    # Update the output grid with the color from the kernel pattern
                    output_grid[pr, pc] = kernel[kernel_row_index, kernel_col_index]

    return output_grid