"""
1.  **Identify the Azure Shape:** Locate the connected shape(s) formed by azure (8) pixels. These shapes are composed of diagonal lines. There can be one or multiple of them.

2.  **Analyze White Pixel Adjacency:** Examine the white (0) pixels that are adjacent to the azure shape(s).

3.  **Conditional Color Change:**
    *   If a white pixel is directly above or below an azure pixel *within the connected azure shape*, change its color to green (3).
    *   If a white pixel is directly to the left or right of an azure pixel *within the connected azure shape*, change its color to yellow (4).
    *   If a white pixel is *only* diagonally adjacent to the azure shape (and not orthogonally adjacent to any part of it), its color remains unchanged (white/0).
    *   Pixels part of the connected azure shape do not change.
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=True):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (abs(i) + abs(j) != 1):
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def get_connected_components(grid, color):
    """
    Finds connected components of a specific color in the grid.  Uses a
    flood-fill algorithm. Does not consider diagonally adjacent pixels to be
    connected.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    def flood_fill(row, col, current_component):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_component.append((row, col))
        # Only check orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            flood_fill(row + dr, col + dc, current_component)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                current_component = []
                flood_fill(row, col, current_component)
                components.append(current_component)
    return components

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Azure shapes
    azure_shapes = get_connected_components(input_grid, 8)

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            # Process only white pixels
            if input_grid[row, col] == 0:
                # Get orthogonal and diagonal neighbors
                orthogonal_neighbors = get_neighbors(input_grid, row, col, include_diagonal=False)
                diagonal_neighbors = get_neighbors(input_grid, row, col, include_diagonal=True)

                is_adjacent_to_azure = False

                # check for orthogonal neighbors
                for n_row, n_col in orthogonal_neighbors:
                    if input_grid[n_row, n_col] == 8:
                        is_adjacent_to_azure = True
                        if n_row == row:  # Left or right
                            output_grid[row, col] = 4  # Yellow
                        elif n_col == col: # Above or below
                            output_grid[row, col] = 3  # Green
                        break # only one transformation

                # if no orthogonal, check all diagonal neighbors, and that the
                # neighbor is part of a shape in azure_shapes
                if not is_adjacent_to_azure:
                    for n_row, n_col in diagonal_neighbors:
                        for shape in azure_shapes:
                            if (n_row, n_col) in shape and input_grid[n_row, n_col] == 8:
                                # only change if no orthogonal neighbor
                                orthogonal_to_shape = False
                                for shape_row, shape_col in shape:
                                    shape_ortho_neighbors = get_neighbors(input_grid, shape_row, shape_col, include_diagonal = False )
                                    if (row, col) in shape_ortho_neighbors:
                                        orthogonal_to_shape = True
                                        break
                                if not orthogonal_to_shape:
                                   continue # don't color this one

    return output_grid