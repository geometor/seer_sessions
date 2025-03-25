"""
1.  **Identify Wall Colors:**
    *   If color `3` (green) is present in the input grid, the wall colors are `8` (azure) and `3` (green).
    *   Otherwise, the wall colors are `8` (azure) and `4` (yellow).

2.  **Identify Wall Pixels:** Locate all pixels in the input grid that match the identified wall colors. These pixels define the boundaries of regions.

3. **Identify Interior Regions for Filling** The areas enclosed *completely* by the identified "wall" pixels constitute the regions to be filled.

4.  **Flood Fill:** Perform a flood fill operation with color `2` (red) within each enclosed region, starting from a seed point *inside* the region. The flood fill should stop at the wall pixels (boundary). Do not fill wall pixels.

5.  **Output:** Return the modified grid. The output grid will have the wall pixels unchanged, and the interior regions filled with red (color 2).
"""

import numpy as np

def get_wall_colors(grid):
    """Determines the wall colors based on the presence of green (3)."""
    if 3 in np.unique(grid):
        return {8, 3}
    else:
        return {8, 4}

def flood_fill(grid, start_row, start_col, fill_color, wall_colors):
    """Performs a flood fill operation."""
    rows, cols = grid.shape
    if (
        start_row < 0
        or start_row >= rows
        or start_col < 0
        or start_col >= cols
        or grid[start_row, start_col] in wall_colors
        or grid[start_row, start_col] == fill_color
    ):
        return

    grid[start_row, start_col] = fill_color
    # Recursively fill adjacent cells
    flood_fill(grid, start_row + 1, start_col, fill_color, wall_colors)
    flood_fill(grid, start_row - 1, start_col, fill_color, wall_colors)
    flood_fill(grid, start_row, start_col + 1, fill_color, wall_colors)
    flood_fill(grid, start_row, start_col - 1, fill_color, wall_colors)



def find_seed_points(grid, wall_colors):
    """
    Finds potential seed points for flood filling.  A seed point is a non-wall
    pixel that is adjacent to a wall pixel, but not in a straight line that makes it likely
    part of an extended border.
    """
    rows, cols = grid.shape
    seed_points = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] not in wall_colors:
                # Check neighbors for wall pixels
                neighbors = []
                if r > 0:
                    neighbors.append(grid[r-1, c])
                if r < rows - 1:
                    neighbors.append(grid[r+1, c])
                if c > 0:
                    neighbors.append(grid[r, c-1])
                if c < cols - 1:
                    neighbors.append(grid[r, c+1])

                wall_neighbor_count = sum(1 for neighbor in neighbors if neighbor in wall_colors)

                if wall_neighbor_count > 0 and wall_neighbor_count < 4 :
                  seed_points.append((r,c))
    return seed_points


def transform(input_grid):
    # Initialize output grid as a copy
    output_grid = np.copy(input_grid)

    # Determine wall colors
    wall_colors = get_wall_colors(output_grid)

    # Fill color
    fill_color = 2
    
    # Find seed points
    seed_points = find_seed_points(output_grid, wall_colors)
    
    # Perform flood fill from each seed point
    for r, c in seed_points:
         flood_fill(output_grid, r, c, fill_color, wall_colors)


    return output_grid