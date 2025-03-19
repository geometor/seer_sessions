"""
1. Identify all distinct gray regions in the input grid. A gray region is a group of one or more orthogonally connected gray pixels.
2. Determine if ANY of the distinct gray regions are connected to each other.  Two regions are considered connected if any pixel in one region shares an orthogonal border (up, down, left, or right) with any pixel in another region.
3. If ANY gray regions are connected, flood fill ALL gray regions with red.
4. If NO gray regions are connected, the gray regions are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the valid neighbors of a cell in a grid (up, down, left, right).
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color):
    """
    Performs a flood fill on the grid starting from (row, col), changing target_color to replacement_color.
    """
    if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]:
        return  # Out of bounds
    if grid[row, col] != target_color:
        return  # Not the target color

    grid[row, col] = replacement_color
    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        flood_fill(grid, r, c, target_color, replacement_color)

def get_gray_regions(grid):
    """
    Identifies and returns a list of distinct gray regions.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    gray_regions = []

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 5 and not visited[row, col]:
                # New gray region found, use flood fill to get its extent
                region_mask = np.zeros_like(grid, dtype=bool)
                flood_fill(region_mask, row, col, 5, True) #temporarily fill with True
                current_region = []
                for r in range(rows):
                    for c in range(cols):
                        if region_mask[r,c] == True:
                            current_region.append((r, c))
                            visited[r,c] = True
                gray_regions.append(current_region)
    return gray_regions

def are_regions_connected(regions, grid):
    """
    Checks if any two regions in the list of regions are connected.
    """
    for i in range(len(regions)):
        for j in range(i + 1, len(regions)):
            for r1, c1 in regions[i]:
                for r2, c2 in regions[j]:
                    if (abs(r1 - r2) == 1 and c1 == c2) or \
                       (abs(c1 - c2) == 1 and r1 == r2):  # Orthogonally adjacent
                        return True
    return False

def transform(input_grid):
    """
    Transforms the input grid based on gray region connectivity.
    """
    output_grid = np.copy(input_grid)
    gray_regions = get_gray_regions(output_grid)

    if are_regions_connected(gray_regions, output_grid):
        # Fill all gray regions with red
        for region in gray_regions:
            for r, c in region:
                output_grid[r, c] = 2
    
    return output_grid