"""
Transforms an input grid into a larger output grid by expanding the original
grid and then applying a complex, context-aware color modification rule. This
rule seems to involve a form of interpolation or smoothing, particularly at
the boundaries between regions of different colors.
"""

import numpy as np

def expand_grid(input_grid, out_rows, out_cols):
    """Expands the input grid to the specified output dimensions."""
    in_rows, in_cols = input_grid.shape
    expanded_grid = np.zeros((out_rows, out_cols), dtype=int)

    for r in range(out_rows):
        for c in range(out_cols):
            # Map output coordinates back to input coordinates (with wrapping)
            in_r = r % in_rows
            in_c = c % in_cols
            expanded_grid[r, c] = input_grid[in_r, in_c]

    return expanded_grid

def modify_pixels(grid):
    """Applies the context-aware color modification."""
    rows, cols = grid.shape
    new_grid = grid.copy()

    for r in range(rows):
        for c in range(cols):
            neighbors = []
            # Collect neighbors (with boundary handling)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    nr, nc = r + i, c + j
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbors.append(grid[nr, nc])

            # Apply a modification rule based on neighbors (this is a placeholder for the *actual* complex rule)
            current_val = grid[r,c]
            if len(neighbors) > 0:
                unique_neighbors = np.unique(neighbors)
                if len(unique_neighbors) > 1: # if there's a mix of neighbors
                    #  Find the most frequent neighbor, not including the current value
                    neighbor_counts = [(val, neighbors.count(val)) for val in unique_neighbors if val != current_val]
                    if len(neighbor_counts)>0:
                        most_frequent_neighbor = max(neighbor_counts, key=lambda item: item[1])[0]
                        new_grid[r,c] = most_frequent_neighbor


    return new_grid



def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_grid = np.array(input_grid)
    in_rows, in_cols = input_grid.shape

    # Determine output dimensions (this is a rough estimate based on the examples)
    out_rows = in_rows * 2 + np.random.randint(-2,3) # add some noise/variablity
    out_cols = int(in_cols * 2.5) + np.random.randint(-2,3) # more noise, non-uniform scaling

    # 1. Expand the grid
    expanded_grid = expand_grid(input_grid, out_rows, out_cols)

    # 2. Modify pixel values based on context
    output_grid = modify_pixels(expanded_grid)

    return output_grid.tolist()