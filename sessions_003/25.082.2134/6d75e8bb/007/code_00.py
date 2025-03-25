"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels in the input grid.

2.  **Identify White Regions:** Find all contiguous regions of white (0) pixels.

3.  **Determine Enclosure:** For each azure region:
    *   An azure region is considered "enclosed" if it has *no* adjacent white (0) pixels.  Adjacency includes diagonals.

4.  **Replace Non-Enclosed Azure Edge Pixels:** Iterate through each azure region. If an azure region is *not* "enclosed":
     - An azure pixel is an "edge" pixel in that region if:
        - It is adjacent to any white pixel (including diagonals) OR
        - It has fewer than 3 adjacent azure neighbors (not including diagonals).
     - Change any "edge" pixels to red (2).
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=False):
    """Returns the neighbors of a pixel."""
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

    if include_diagonal:
        if row > 0 and col > 0:
            neighbors.append((row-1, col-1))
        if row > 0 and col < cols -1:
            neighbors.append((row-1, col+1))
        if row < rows - 1 and col > 0:
            neighbors.append((row + 1, col -1 ))
        if row < rows -1 and col < cols - 1:
            neighbors.append((row+1, col+1))
    return neighbors

def find_regions(grid, color):
    """Finds contiguous regions of a specific color."""
    regions = []
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, current_region):
        if (row, col) in visited or grid[row, col] != color:
            return
        visited.add((row, col))
        current_region.append((row, col))
        for r, c in get_neighbors(grid, row, col):
            dfs(r, c, current_region)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and (row, col) not in visited:
                current_region = []
                dfs(row, col, current_region)
                regions.append(current_region)
    return regions

def is_adjacent_to_color(grid, region, color):
    """Checks if a region is adjacent to a pixel of a specific color (including diagonals)."""
    for row, col in region:
        for r, c in get_neighbors(grid, row, col, include_diagonal=True):
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == color:
                return True
    return False

def is_enclosed(grid, region):
    """Checks if an azure region is enclosed (not adjacent to white)."""
    return not is_adjacent_to_color(grid, region, 0)

def get_edge_pixels(grid, region):
    """Gets the edge pixels of a non-enclosed azure region."""
    edge_pixels = set()
    for row, col in region:
        # Adjacent to white
        if is_adjacent_to_color(grid, [(row, col)], 0):
            edge_pixels.add((row, col))
            continue

        # Fewer than 3 azure neighbors
        azure_neighbors = 0
        for r, c in get_neighbors(grid, row, col):
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 8:
                azure_neighbors += 1
        if azure_neighbors < 3:
            edge_pixels.add((row, col))

    return edge_pixels

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    # 1. Identify Azure Regions
    azure_regions = find_regions(input_grid, 8)

    # 2. Identify White Regions
    white_regions = find_regions(input_grid, 0) #Not used directly, but kept per the NL program

    # 3. Determine Enclosure & 4. Replace
    for region in azure_regions:
        if not is_enclosed(input_grid, region):
            edge_pixels = get_edge_pixels(input_grid, region)
            for row, col in edge_pixels:
                output_grid[row, col] = 2

    return output_grid.tolist()