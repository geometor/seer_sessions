"""
1.  **Identify Red Regions:** Find all contiguous groups of red (2) pixels in the input grid.  These can be single pixels or larger connected shapes.
2.  **For Each Red Region:**
    *   **Find Connected White Regions:** Identify all white (0) pixels that are directly *or indirectly* connected to the red region.  Connectivity includes horizontal, vertical, and diagonal adjacency. This forms a "white region" connected to the "red region".
    *   **Flood Fill:** Change the color of all pixels within the connected white region to yellow (4). This is a recursive process:
        *   Start with white pixels directly adjacent to the red region.
        *   For each newly colored yellow pixel, check its neighbors.
        *   Continue until no more connected white pixels are found.
3. **Repeat:** Perform steps 2.1 and 2.2 for *each* distinct red region found in the grid.
4.  **Output:** The resulting grid, with white regions adjacent to red regions now filled with yellow, is the output.
"""

import numpy as np

def get_red_regions(grid):
    """
    Finds all contiguous red regions in the grid.
    Uses a depth-first search approach.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    red_regions = []

    def dfs(row, col, current_region):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != 2):
            return
        visited[row, col] = True
        current_region.append((row, col))
        # Explore all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc, current_region)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2 and not visited[r, c]:
                current_region = []
                dfs(r, c, current_region)
                red_regions.append(current_region)
    return red_regions

def flood_fill(grid, start_row, start_col, target_color, replacement_color):
    """
    Performs a flood fill operation on the grid.
    """
    rows, cols = grid.shape
    if (start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols or
            grid[start_row, start_col] != target_color):
        return
    grid[start_row, start_col] = replacement_color
    # Explore all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            flood_fill(grid, start_row + dr, start_col + dc, target_color, replacement_color)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    red_regions = get_red_regions(output_grid)

    for region in red_regions:
        # Find adjacent white pixels for each red region
        adjacent_whites = set()
        for r, c in region:
            rows, cols = output_grid.shape
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue  # Skip the cell itself
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                        adjacent_whites.add((nr, nc))
        # Flood fill from the adjacent white pixels
        for r, c in adjacent_whites:
            flood_fill(output_grid, r, c, 0, 4)


    return output_grid