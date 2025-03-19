"""
Change the color of enclosed azure (8) regions to green (3), within the bounding shape of blue (1) pixels.
"""

import numpy as np

def find_contiguous_regions(grid, color):
    """Finds contiguous regions of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_region.append((row, col))
        dfs(row + 1, col, current_region)
        dfs(row - 1, col, current_region)
        dfs(row, col + 1, current_region)
        dfs(row, col - 1, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_region_enclosed(grid, region, enclosing_color):
    """Checks if a region is entirely enclosed by a specified color."""
    rows, cols = grid.shape
    for row, col in region:
        # Check neighbors (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n_row, n_col in neighbors:
            if not (0 <= n_row < rows and 0 <= n_col < cols):
                continue # consider edge of grid as "not enclosed"
            if grid[n_row, n_col] != enclosing_color:
                #also check diagonal
                diag_neighbors = [(row - 1, col - 1), (row - 1, col + 1), (row+1, col-1), (row+1, col+1)]
                valid_diag = False
                for d_row, d_col in diag_neighbors:
                    if not (0 <= d_row < rows and 0 <= d_col < cols):
                        continue
                    if grid[d_row,d_col] == enclosing_color:
                        valid_diag = True
                        break
                if not valid_diag and grid[n_row,n_col] != 8:
                    return False  # Found a neighbor that isn't the enclosing color
    return True

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = input_grid.copy()
    azure_regions = find_contiguous_regions(output_grid, 8)

    for region in azure_regions:
        if is_region_enclosed(output_grid, region, 1):
            # Replace some of the azure (8) with green (3)
            for r, c in region:
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                num_azure = 0
                for nr, nc in neighbors:
                    if not (0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1]):
                        continue
                    if output_grid[nr,nc] == 8:
                        num_azure += 1

                if num_azure < 4 and num_azure > 0:
                     output_grid[r,c] = 3
    return output_grid