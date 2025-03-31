```python
import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the non-background pixels
    in each row to the left. The amount of shift for a given row
    is determined by the column index of the left-most non-background
    pixel in that row, such that this pixel ends up in column 0
    in the output grid. Rows containing only background pixels remain
    unchanged.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid with the same dimensions, filled with the background color (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row of the input grid
    for r in range(height):
        # Get the current row
        row = input_grid[r, :]

        # Find the indices of non-background (non-zero) pixels in the current row
        non_zero_indices = np.where(row != 0)[0]

        # If there are no non-zero pixels, the row is entirely background
        if len(non_zero_indices) == 0:
            # Copy the background row directly (already initialized to 0, so technically optional)
            # output_grid[r, :] = 0 
            continue # Proceed to the next row
        else:
            # Find the column index of the first (left-most) non-zero pixel
            first_col_index = non_zero_indices[0]

            # Calculate the horizontal shift amount needed to move the first non-zero pixel to column 0
            shift = -first_col_index

            # Iterate through the pixels of the current input row
            for c in range(width):
                # Get the color of the pixel
                color = input_grid[r, c]

                # If the pixel is not background
                if color != 0:
                    # Calculate the new column index after applying the shift
                    new_col = c + shift
                    
                    # Ensure the new column index is within the grid bounds
                    # (Should always be true with this logic, but good practice)
                    if 0 <= new_col < width:
                        # Place the pixel's color at the new position in the output grid
                        output_grid[r, new_col] = color

    # Return the completed output grid
    return output_grid
```