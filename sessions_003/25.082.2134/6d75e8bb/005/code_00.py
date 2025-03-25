"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels in the input grid.
2.  **Identify White Regions:** Find all contiguous regions of white (0) pixels.
3.  **Determine Enclosure:** For each azure region:
    *   Check if the azure region is adjacent to a white region.
    *   An azure region is considered "enclosed" if it has *no* adjacent white pixels, *and* all of its azure pixels have at least 3 neighboring pixels which are either the edge of the image or another azure.
4.  **Replace Non-Enclosed Azure:** Iterate through each azure region. If an azure region is *not* "enclosed", change all the azure pixels on the "edge" to red (2), where edge means they are adjacent to a 0 or have fewer than 3 azure neighbors.
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
    """Checks if a region is adjacent to a pixel of a specific color."""
    for row, col in region:
        for r, c in get_neighbors(grid, row, col):
            if grid[r, c] == color:
                return True
    return False

def is_enclosed(grid, region):
    """Checks if an azure region is enclosed."""
    if is_adjacent_to_color(grid, region, 0):
        return False

    rows, cols = grid.shape

    for row, col in region:
        neighbor_count = 0
        for r, c in get_neighbors(grid, row, col):
            if grid[r,c] == 8:
               neighbor_count +=1
        if neighbor_count < 3:
            # also consider out of bounds as a neighbor, as long as we aren't touching color 0
            out_of_bounds_neighbors = 0
            if row == 0: out_of_bounds_neighbors+=1
            if col == 0: out_of_bounds_neighbors += 1
            if row == rows -1: out_of_bounds_neighbors += 1
            if col == cols -1: out_of_bounds_neighbors +=1

            for nr, nc in get_neighbors(grid, row, col, include_diagonal=True):
                if not (0 <= nr < rows and 0 <= nc < cols):
                   continue
                if grid[nr,nc] == 0:
                   return False
            
            if neighbor_count + out_of_bounds_neighbors < 3 and not is_adjacent_to_color(grid, [(row,col)], 0):
                return False


    return True
def get_edge_pixels(grid, region):
    """get the edge pixels of a region"""
    edge_pixels = set()
    rows,cols = grid.shape
    for row, col in region:
        if is_adjacent_to_color(grid, [(row,col)], 0):
            edge_pixels.add((row,col))
            continue
        
        neighbor_count = 0
        for r, c in get_neighbors(grid, row, col):
            if grid[r,c] == 8:
                neighbor_count +=1
        if neighbor_count < 3:
           edge_pixels.add((row,col))
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
    white_regions = find_regions(input_grid, 0)

    # 3. Determine Enclosure & 4. Replace
    for region in azure_regions:
        if not is_enclosed(input_grid, region):
            for row, col in get_edge_pixels(input_grid, region):
                output_grid[row, col] = 2
    return output_grid.tolist()