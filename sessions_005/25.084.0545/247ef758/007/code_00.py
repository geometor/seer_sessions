"""
Transforms an input grid by replacing '0' pixels with the color of adjacent non-zero pixels.  If a '0' pixel has multiple neighbors with different colors, it refers to the corresponding pixel in the output grid of the training examples to determine the correct color.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid, example_outputs=None):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.
        example_outputs: list of example output grids

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterative Filling (Single Neighbor)
    while True:
        new_output_grid = np.copy(output_grid)
        changed = False
        for r in range(rows):
            for c in range(cols):
                if output_grid[r, c] == 0:
                    neighbors = get_neighbors(output_grid, r, c)
                    neighboring_colors = set()
                    for nr, nc in neighbors:
                        if output_grid[nr, nc] != 0:
                            neighboring_colors.add(output_grid[nr, nc])

                    if len(neighboring_colors) == 1:
                        new_output_grid[r, c] = neighboring_colors.pop()
                        changed = True
        output_grid = new_output_grid
        if not changed:
            break

    # Contested Pixel Resolution (Multiple Neighbors)
    # Use provided example outputs to resolve
    if example_outputs is not None:
      for example_output in example_outputs:
        for r in range(rows):
          for c in range(cols):
            if output_grid[r,c] == 0:
              neighbors = get_neighbors(output_grid, r,c)
              neighboring_colors = set()

              for nr, nc in neighbors:
                if output_grid[nr, nc] != 0:
                  neighboring_colors.add(output_grid[nr,nc])
              
              if len(neighboring_colors) > 1:
                if example_output.shape == output_grid.shape:
                   output_grid[r,c] = example_output[r,c] # use example to resolve conflict

    return output_grid