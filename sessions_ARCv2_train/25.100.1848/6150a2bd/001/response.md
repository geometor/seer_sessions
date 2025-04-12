```python
import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by rotating it 180 degrees.

    Each element at position [row][col] in the input grid is moved to
    position [N - 1 - row][M - 1 - col] in the output grid, where N is the
    total number of rows and M is the total number of columns.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions (number of rows N, number of columns M)
    n_rows, n_cols = input_array.shape

    # Initialize the output grid with zeros, same dimensions as input
    output_array = np.zeros_like(input_array)

    # Iterate through each element of the input grid
    for r in range(n_rows):
        for c in range(n_cols):
            # Calculate the target position in the output grid for 180-degree rotation
            target_row = n_rows - 1 - r
            target_col = n_cols - 1 - c

            # Assign the value from the input grid to the target position in the output grid
            output_array[target_row, target_col] = input_array[r, c]

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```