```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    Iterate through each pixel in the input grid.
    If a pixel is green (color 3), check its four orthogonal neighbors (up, down, left, right).
    If any of these neighbors are also green (color 3), change the current pixel's color to azure (color 8) in the output grid.
    Otherwise, the pixel retains its original color in the output grid.
    Pixels that are not green (not color 3) remain unchanged.
    The output grid has the same dimensions as the input grid.
    """

    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to store the output, so we don't modify the grid while iterating
    output_grid = np.copy(input_np)
    # Get the dimensions of the grid
    rows, cols = input_np.shape

    # Define the relative coordinates for orthogonal neighbors (up, down, left, right)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Iterate through each cell (pixel) in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell's color is green (3)
            if input_np[r, c] == 3:
                has_green_neighbor = False
                # Check each orthogonal neighbor
                for dr, dc in neighbors:
                    # Calculate neighbor coordinates
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor's coordinates are within the grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor's color is green (3)
                        if input_np[nr, nc] == 3:
                            has_green_neighbor = True
                            # If a green neighbor is found, no need to check further neighbors for this cell
                            break

                # If at least one green orthogonal neighbor was found,
                # change the color of the current cell in the output grid to azure (8)
                if has_green_neighbor:
                    output_grid[r, c] = 8
            # If the cell is not green, or if it's green but has no green neighbors,
            # its value in the output_grid remains unchanged (as it was copied from input_np).

    # Convert the resulting NumPy array back to a list of lists before returning
    return output_grid.tolist()

```