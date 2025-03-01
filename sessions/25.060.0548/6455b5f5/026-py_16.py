"""
1.  **Identify the Red Shape:** Locate all red (2) pixels in the input grid. These pixels form a single connected shape.

2.  **Identify Enclosed Regions:** Within the red shape, find all regions consisting of white (0) pixels that are completely surrounded by red pixels. A region is considered enclosed if *none* of its pixels are adjacent to the edge of the grid.

3.  **Count and Sort:** Count the number of enclosed white regions. If there is only one, change all its pixels to azure (8).

4. **Fill based on count**
    If there are multiple regions:
      - Determine the *smallest* enclosed region by the number of its pixels.
      - Change all pixels in the smallest region to azure (8).
      - Change all pixels in the *remaining* enclosed regions to blue (1).

5.  **Background:** All other pixels (those not part of any enclosed white region) retain their original colors.
"""

import numpy as np

def find_connected_components(grid, color):
    """Finds connected components of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(row, col, current_component):
        """Depth-First Search to explore connected component."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return

        visited[row, col] = True
        current_component.append((row, col))

        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_component = []
                dfs(row, col, current_component)
                components.append(current_component)
    return components

def find_enclosed_regions(grid, enclosing_color):
    """
    Finds regions of white (0) pixels enclosed by the enclosing_color.
    A region is enclosed if none of its pixels touch the grid edge.
    """
    rows, cols = grid.shape
    enclosed_regions = []
    visited = set()

    def is_enclosed(region):
        """Checks if a region is fully enclosed (not touching the edge)."""
        for row, col in region:
            if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                return False
        return True

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # Only process white (0) cells
            if grid[r,c] == 0 and (r,c) not in visited:
                q = [(r,c)]
                visited.add((r,c))
                region_cells = []

                while q:
                    row, col = q.pop()
                    region_cells.append((row, col))

                    neighbors = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]

                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr, nc] == 0 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                            # No need to check for the enclosing color here

                if is_enclosed(region_cells):
                    enclosed_regions.append(region_cells)

    return enclosed_regions


def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)

    # 1. Identify the Red Shape (already done in find_enclosed_regions)

    # 2. Identify Enclosed Regions
    enclosed_regions = find_enclosed_regions(output_grid, 2)

    # 3. Count and Sort
    if enclosed_regions:
        if len(enclosed_regions) == 1:
            # If only one enclosed region, fill with azure
            for row, col in enclosed_regions[0]:
                output_grid[row, col] = 8
        else:
            # 4. Fill based on count (multiple regions)
            enclosed_regions.sort(key=len)  # Sort by size (smallest first)
            for row, col in enclosed_regions[0]:
                output_grid[row, col] = 8  # Smallest to azure
            for region in enclosed_regions[1:]:
                for row, col in region:
                    output_grid[row, col] = 1  # Others to blue

    # 5. Background remains unchanged (handled by copying)
    return output_grid