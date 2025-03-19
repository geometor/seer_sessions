"""
The transformation rule is as follows:
1. Locate the single blue (1) cell within the input grid.
2. Create an output grid of the same dimensions as the input, initialized with zeros.
3. Copy the value of the blue cell (1) from the input to the same position in the output.
4. Perform an alternating expansion:
   - Cells adjacent to blue (1) cells become azure (8) if they are white (0).
   - Cells adjacent to azure (8) cells become blue (1) if they are white (0).
5. This expansion continues until the entire grid is filled with an alternating pattern of azure (8) and blue (1).
"""

import numpy as np

def get_seed_position(grid):
    # Find the coordinates of the blue (1) cell.
    coords = np.where(grid == 1)
    return coords[0][0], coords[1][0]

def is_valid(r, c, grid):
    # Check if row, col are within the grid boundaries
    rows, cols = grid.shape
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid):
    # initialize output_grid with zeros and the same dimensions
    output_grid = np.zeros_like(input_grid)

    # get seed position
    seed_r, seed_c = get_seed_position(input_grid)
    output_grid[seed_r, seed_c] = 1

    # Create a queue for cells to be processed, initialized with seed position
    queue = [(seed_r, seed_c)]

    # Loop to change output pixels
    while queue:
        r, c = queue.pop(0)  # Dequeue a cell
        current_color = output_grid[r,c]

        # Define neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for nr, nc in neighbors:
            if is_valid(nr, nc, output_grid):
                if output_grid[nr, nc] == 0: #if white
                    if current_color == 1:
                        output_grid[nr, nc] = 8  # white adjacent to 1 becomes 8
                        queue.append((nr, nc))
                    elif current_color == 8:
                        output_grid[nr, nc] = 1 # white adjacent to 8 becomes 1
                        queue.append((nr, nc))

    return output_grid