"""
1.  **Identify Gray Regions:** Find all contiguous regions of gray (5) pixels in the input grid. Diagonally connected gray pixels are considered part of the same region.

2.  **Determine Enclosure:** For each gray region, determine if it's fully enclosed. A region is considered fully enclosed if and only if all non-gray pixels within its bounding box are completely surrounded, including diagonals, by either gray pixels belonging to that region or the edge of the entire grid. This means there are no "leaks" to the outside.

3.  **Fill Enclosed Interiors:** If a gray region is fully enclosed, change the color of all non-gray pixels *inside* the region to red (2). A non-gray pixel is considered "inside" if it is within the bounding box defined by the gray region, and all eight neighboring pixels (including diagonals) are either: (a) gray pixels that are part of the *same* contiguous gray region, or (b) outside the bounds of the entire input grid. Specifically, *do not* change gray pixels that are found inside a larger gray object.

4.  **Leave Other Regions Unchanged:** Gray regions that are not fully enclosed (i.e., have a "leak" to the outside) should remain unchanged, as should any gray pixels within the enclosing region.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid, including diagonals."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        """Depth-first search to explore contiguous regions, including diagonals."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_region.append((row, col))
        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_fully_enclosed(region, grid):
    """
    Checks if a region is fully enclosed within the grid. A region is enclosed
    if all non-gray pixels within its bounding box are surrounded by gray pixels
    of the *same* region or the grid boundary.
    """
    if not region:
        return False

    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Iterate through all cells within the bounding box
    for r in range(min_row -1, max_row + 2):
        for c in range(min_col - 1, max_col + 2):
            # Consider only the cells within grid
            if 0 <= r < grid.shape[0] and 0<= c < grid.shape[1]:
                # if outside the region and not gray, check for leak
                if (r,c) not in region and grid[r,c] != 5:
                    # check if the current cell is leaking
                    is_leaking = False
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            # if neighbor is outside the grid and current cell is not gray, it is leaking
                            if nr < 0 or nr >= grid.shape[0] or nc < 0 or nc >= grid.shape[1]:
                                is_leaking = True
                                break
                            # if neighbor is not gray and not in region, it's leaking
                            if grid[nr, nc] != 5 and (nr, nc) not in region:
                                is_leaking = True
                                break
                        if is_leaking:
                            break
                    if is_leaking: return False
    return True
    

def get_inner_pixels(region, grid):
    """
    Gets the inner pixels of a fully enclosed region, excluding gray pixels of the region itself.
    """
    rows, cols = zip(*region)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    inner_pixels = []
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if (r, c) not in region:  # Only consider non-gray pixels within the bounding box
                is_inner = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if (nr, nc) not in region:  # Check neighbors
                            if nr < 0 or nr >= grid.shape[0] or nc < 0 or nc >= grid.shape[1]:
                                continue  # Grid boundary is considered part of the enclosure
                            else:
                                is_inner = False  # Not surrounded by region or boundary
                                break
                    if not is_inner:
                        break
                if is_inner:
                    inner_pixels.append((r, c))
    return inner_pixels

def transform(input_grid):
    """
    Identifies contiguous regions of gray (5) pixels.
    If a gray region is fully enclosed, changes the color of inner non-gray pixels to red.
    """
    output_grid = np.copy(input_grid)
    gray_regions = find_contiguous_regions(input_grid, 5)

    for region in gray_regions:
        if is_fully_enclosed(region, input_grid):
            inner_pixels = get_inner_pixels(region, input_grid)
            for row, col in inner_pixels:
                output_grid[row, col] = 2  # Red

    return output_grid