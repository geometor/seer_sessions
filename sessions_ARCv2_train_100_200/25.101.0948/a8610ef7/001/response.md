```python
"""
Transforms an input grid based on the following rules:
1. White (0) pixels remain white (0).
2. Azure (8) pixels are transformed based on their neighbors:
   - Count the number of azure (8) neighbors in the 8 adjacent cells (including diagonals).
   - If the count of azure neighbors is odd, the output pixel becomes red (2).
   - If the count of azure neighbors is even, the output pixel becomes gray (5).
"""

import numpy as np

def count_azure_neighbors(grid: np.ndarray, r: int, c: int) -> int:
    """
    Counts the number of azure (8) neighbors for a given cell (r, c).
    Handles boundary conditions.
    """
    height, width = grid.shape
    count = 0
    # Iterate through the 3x3 neighborhood
    for i in range(max(0, r - 1), min(height, r + 2)):
        for j in range(max(0, c - 1), min(width, c + 2)):
            # Skip the center cell itself
            if i == r and j == c:
                continue
            # Check if the neighbor is azure
            if grid[i, j] == 8:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid with the same dimensions, filled with zeros initially
    output_array = np.zeros_like(input_array)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_array[r, c]

            # Rule 1: Preserve white pixels
            if pixel_color == 0:
                output_array[r, c] = 0
            # Rule 2: Transform azure pixels based on neighbor count
            elif pixel_color == 8:
                # Count azure neighbors
                neighbor_count = count_azure_neighbors(input_array, r, c)

                # Apply transformation based on parity of neighbor count
                if neighbor_count % 2 != 0:  # Odd count
                    output_array[r, c] = 2  # Red
                else:  # Even count (including 0)
                    output_array[r, c] = 5  # Gray
            # Handle any unexpected colors (though the problem description implies only 0 and 8)
            else:
                 output_array[r, c] = pixel_color # Or handle as an error, based on assumptions


    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_array.tolist()

    return output_grid
```