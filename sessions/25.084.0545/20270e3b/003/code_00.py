"""
The transformation rule involves identifying and preserving the largest outer rectangular boundary formed by color 4 (yellow)
and any contiguous inner region of color 1 (blue) connected to this boundary, while removing all pixels of color 7 (orange).
If there is a break due to orange, then only keep the section before the break.
"""

import numpy as np
from scipy.ndimage import measurements

def find_outer_rectangle(grid, color):
    """Finds the coordinates of the largest outer rectangle of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_connected_component(grid, start_row, start_col, color):
    """Gets all pixels connected to the start using Breadth First Search"""

    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    pixels = []
    queue = [(start_row, start_col)]
    visited[start_row, start_col] = True

    while queue:
        row, col = queue.pop(0)
        pixels.append((row,col))

        # Check neighbors (up, down, left, right)
        neighbors = []
        if row > 0:
            neighbors.append( (row - 1, col))
        if row < rows - 1:
            neighbors.append( (row + 1, col) )
        if col > 0:
            neighbors.append( (row, col - 1))
        if col < cols - 1:
            neighbors.append( (row, col + 1) )

        for n_row, n_col in neighbors:
            if not visited[n_row, n_col] and grid[n_row, n_col] == color:
                visited[n_row, n_col] = True
                queue.append((n_row, n_col))
            elif not visited[n_row, n_col] and grid[n_row,n_col] != 0: #check other colors connected
                if grid[n_row,n_col] != 7: #check if is not orange
                    visited[n_row, n_col] = True
                    queue.append((n_row,n_col))

    return pixels

def transform(input_grid):
    """Transforms the input grid by keeping the outer yellow rectangle and connected blue pixels."""

    input_grid = np.array(input_grid)
    yellow_rect = find_outer_rectangle(input_grid, 4)

    if yellow_rect is None:
        return input_grid.tolist()  # No transformation if no yellow rectangle

    (min_row, min_col), (max_row, max_col) = yellow_rect
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    #fill output grid with yellow and blue pixels
    for i in range(min_row, max_row+1):
        for j in range(min_col, max_col + 1):
            if input_grid[i,j] == 4:
                output_grid[i-min_row,j-min_col] = 4
            elif input_grid[i,j] == 1:
                 # Get connected component from the boundary.
                connected_pixels = []

                #check top
                if i > 0 and input_grid[i-1,j] == 4:
                    connected_pixels.extend(get_connected_component(input_grid,i,j,1))

                #check bottom
                if i < input_grid.shape[0]-1 and input_grid[i+1,j] == 4:
                    connected_pixels.extend(get_connected_component(input_grid, i, j, 1))

                #check left
                if j > 0 and input_grid[i, j-1] == 4:
                    connected_pixels.extend(get_connected_component(input_grid, i, j, 1))

                #check right
                if j < input_grid.shape[1]-1 and input_grid[i,j+1] == 4:
                        connected_pixels.extend(get_connected_component(input_grid, i, j, 1))

                if len(connected_pixels) > 0:
                    for r,c in connected_pixels:
                        if min_row <= r <= max_row and min_col <= c <= max_col:
                            output_grid[r-min_row,c-min_col] = 1

    return output_grid.tolist()