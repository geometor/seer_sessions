```python
import numpy as np

"""
Iterate through each pixel of the input grid. If a pixel is orange (7), check its eight neighbors (including diagonals). If at least one neighbor exists within the grid boundaries and has a color other than orange (7), change the pixel's color to magenta (6) in the output grid. Otherwise, keep the pixel's original color. Pixels that are not initially orange (7) retain their original color in the output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the neighborhood rule for orange pixels.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input grid to a NumPy array for easier manipulation and indexing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Create an output grid initialized as a copy of the input grid
    # We will modify this grid where necessary
    output_np = np.copy(input_np)

    # Define the color constants
    ORANGE = 7
    MAGENTA = 6

    # Iterate through each cell (pixel) in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is orange
            if input_np[r, c] == ORANGE:
                has_non_orange_neighbor = False
                # Check all 8 neighbors (Moore neighborhood)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the center cell itself
                        if dr == 0 and dc == 0:
                            continue

                        # Calculate neighbor coordinates
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor is within the grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if the neighbor's color is not orange
                            if input_np[nr, nc] != ORANGE:
                                has_non_orange_neighbor = True
                                break  # Found one, no need to check others
                    if has_non_orange_neighbor:
                        break # Exit outer loop as well

                # If at least one non-orange neighbor was found, change the output pixel to magenta
                if has_non_orange_neighbor:
                    output_np[r, c] = MAGENTA
            # If the pixel is not orange, it retains its original color (already copied)

    # Convert the output NumPy array back to a list of lists before returning
    return output_np.tolist()
```