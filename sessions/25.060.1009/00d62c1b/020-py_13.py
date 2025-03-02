"""
1.  **Identify Green Regions:** Find all contiguous regions of green (value 3) pixels in the input grid.  A region is defined as a set of green pixels connected by 8-way adjacency.
2.  **Check for Closure:** For each identified green region, determine if it is "closed." A region is closed if all of its pixels are completely surrounded by non-green pixels within the grid boundaries. If any green pixel in a region touches the edge of the grid, the region isn't closed.
3.  **Conditional Filling:** If and *only if* a green region is determined to be closed, fill the interior of that region with yellow (value 4). The interior pixels are green pixels within a closed region and completely surrounded by other green pixels of that same region.
4. **Output:** Create an output grid. If there are no green regions, output should be same as input. Copy not modified regions from input to output.
"""

import numpy as np

def get_contiguous_pixels(grid, start_pixel, color):
    """
    Finds all pixels contiguous to a starting pixel of a given color using 8-neighbor adjacency.

    Args:
        grid: The 2D numpy array.
        start_pixel: (row, col) tuple.
        color: The color value to match.

    Returns:
        A set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    to_visit = {start_pixel}

    while to_visit:
        current_pixel = to_visit.pop()
        visited.add(current_pixel)

        row, col = current_pixel
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    if (new_row, new_col) not in visited and grid[new_row, new_col] == color:
                        to_visit.add((new_row, new_col))
    return visited

def is_closed_region(grid, region_pixels):
    """
    Checks if a set of pixels forms a closed region.
    """
    rows, cols = grid.shape
    for r, c in region_pixels:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nr, nc = r + i, c + j
                if not (0 <= nr < rows and 0 <= nc < cols):
                    return False  # Touches boundary, not closed
                if grid[nr, nc] != 3:
                    continue #neighbor is not green, keep searching

    return True

def find_internal_pixels(grid, region_pixels):
    """
    Identifies internal pixels within a closed region.
    """
    if not is_closed_region(grid, region_pixels):
      return set()

    min_row = min(r for r, _ in region_pixels)
    max_row = max(r for r, _ in region_pixels)
    min_col = min(c for _, c in region_pixels)
    max_col = max(c for _, c in region_pixels)

    internal_pixels = set()
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if (r, c) in region_pixels:
                is_surrounded = True
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        nr, nc = r + i, c + j
                        if (nr, nc) not in region_pixels:
                            is_surrounded = False
                            break
                    if not is_surrounded:
                        break
                if is_surrounded:
                    internal_pixels.add((r, c))
    return internal_pixels

def transform(input_grid):
    """
    Transforms the input grid by filling the interior of closed green regions with yellow.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Green Regions
    green_pixels = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                green_pixels.add((r, c))

    if not green_pixels:
        return output_grid  # No green pixels, return original grid

    visited_pixels = set()
    distinct_regions = []
    for pixel in green_pixels:
        if pixel not in visited_pixels:
            region = get_contiguous_pixels(input_grid, pixel, 3)
            distinct_regions.append(region)
            visited_pixels.update(region)

    # 2. & 3. Check for Closure and Conditionally Fill
    for region in distinct_regions:
        # if is_closed_region(input_grid, region): # Check moved to find_internal_pixels function
        internal_pixels = find_internal_pixels(input_grid, region)
        for r, c in internal_pixels:
            output_grid[r, c] = 4

    return output_grid