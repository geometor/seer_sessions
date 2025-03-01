"""
1.  **Identify the "cross" shape:** Locate the contiguous block of white (0) pixels that form a "+" shape within the input grid.

2.  **Identify cross neighbors:** Find the colors that appear in the cross shape.

3.  **Identify the background color:** Determine the color that occupies the majority of the grid, excluding the cross.

4.  **Propagate color changes:** Iterate over cross colored pixels. Extend the color diagonally outwards.

5. **Return Grid**
"""

import numpy as np

def find_cross(grid):
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == 0 and
                grid[r-1, c] == 0 and
                grid[r+1, c] == 0 and
                grid[r, c-1] == 0 and
                grid[r, c+1] == 0):
                return r, c  # Return coordinates of the center of the cross
    return None

def get_background_color(grid, cross_center):
    # Create a masked array where the cross is masked out
     mask = np.ones(grid.shape, dtype=bool)
     r, c = cross_center
     mask[r,c] = False
     mask[r-1,c]=False
     mask[r+1,c]=False
     mask[r,c-1]=False
     mask[r,c+1]=False

     masked_grid = np.ma.masked_array(grid, ~mask)

     unique_colors, counts = np.unique(masked_grid.compressed(), return_counts=True)

     if len(counts) > 0:  # Make sure the grid is not completely empty
         background_color = unique_colors[np.argmax(counts)]
         return background_color
     else:
         return None

def get_cross_neighbors(grid, cross_center):
    r, c = cross_center
    neighbors = []
    if grid[r-1,c] == 0:
       if r > 1:
          neighbors.append((r-2,c))
    if grid[r+1,c] == 0:
       if r < grid.shape[0]-2:
          neighbors.append((r+2, c))
    if grid[r,c-1] == 0:
        if c > 1:
           neighbors.append((r,c-2))
    if grid[r,c+1] == 0:
       if c < grid.shape[1] - 2:
          neighbors.append((r,c+2))

    colors = [grid[nr,nc] for nr, nc in neighbors if grid[nr,nc] != 0]

    return colors, neighbors
def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = grid.copy()

    # 1. Identify the "cross" shape
    cross_center = find_cross(grid)
    if cross_center is None:
        return output_grid #if no cross return grid

    # 2. get cross neighbors and colors
    neighbor_colors, neighbors = get_cross_neighbors(grid, cross_center)

    # 3. Identify the background color
    background_color = get_background_color(grid, cross_center)

   # 4. Propagate neighbor colors diagonally
    for (nr, nc), color in zip(neighbors, neighbor_colors):

        # Extend diagonally upwards and to the left
        dr, dc = nr, nc
        while dr >= 0 and dc >= 0:
            output_grid[dr, dc] = color
            dr -= 1
            dc -= 1

        # Extend diagonally upwards and to the right
        dr, dc = nr, nc
        while dr >= 0 and dc < output_grid.shape[1]:
            output_grid[dr, dc] = color
            dr -= 1
            dc += 1

        # Extend diagonally downwards and to the left
        dr, dc = nr, nc
        while dr < output_grid.shape[0] and dc >= 0:
            output_grid[dr, dc] = color
            dr += 1
            dc -= 1

        # Extend diagonally downwards and to the right
        dr, dc = nr, nc
        while dr < output_grid.shape[0] and dc < output_grid.shape[1]:
            output_grid[dr, dc] = color
            dr += 1
            dc += 1


    return output_grid.tolist()