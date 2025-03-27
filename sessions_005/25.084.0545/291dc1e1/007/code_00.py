"""
Extracts and rearranges contiguous color regions (excluding 0, 1, and 2) from the input grid, forming a smaller output grid.
The first two rows of the input grid are ignored. The spatial relationship of the extracted color regions are maintained as they are arranged, top to bottom and left to right. For each region, two rows of the color are added to the output with a width equal to the horizontal width of the region.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, r - 1), min(rows, r + 2)):
        for j in range(max(0, c - 1), min(cols, c + 2)):
            if (i, j) != (r, c):
                neighbors.append((i, j))
    return neighbors

def extract_regions(grid):
    """Extracts contiguous color regions (excluding 0, 1, and 2), ordered by top-left corner."""
    rows, cols = grid.shape
    visited = set()
    regions = []

    for r in range(2, rows):  # Start from the third row
        for c in range(cols):
            color = grid[r, c]
            if (r, c) not in visited and color not in [0, 1, 2]:
                region = []
                queue = [(r, c)]
                visited.add((r, c))

                while queue:
                    curr_r, curr_c = queue.pop(0)
                    region.append((curr_r, curr_c))
                    for nr, nc in get_neighbors(grid, curr_r, curr_c):
                        if (nr, nc) not in visited and grid[nr, nc] == color:
                            queue.append((nr, nc))
                            visited.add((nr, nc))
                if region:
                    regions.append((color, region))

    # Sort regions by top-left corner (row first, then column)
    regions.sort(key=lambda x: (min(coord[0] for coord in x[1]), min(coord[1] for coord in x[1])))
    return regions

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    
    input_grid = np.array(input_grid)
    regions = extract_regions(input_grid)

    # Calculate output grid dimensions - find max width, and 2 rows per region
    max_width = 0
    for _, region_coords in regions:
      min_col = min(c for _, c in region_coords)
      max_col = max(c for _, c in region_coords)
      max_width = max(max_width, max_col - min_col + 1)

    output_rows = len(regions) * 2
    output_grid = np.zeros((output_rows, max_width), dtype=int)

    # Fill output grid
    current_row = 0
    for color, region_coords in regions:
        min_col = min(c for _, c in region_coords)
        max_col = max(c for _, c in region_coords)
        width = max_col - min_col + 1

        # add two rows for this region
        for i in range(width):
            output_grid[current_row, i] = color
            output_grid[current_row + 1, i] = color
        current_row += 2


    return output_grid.tolist()