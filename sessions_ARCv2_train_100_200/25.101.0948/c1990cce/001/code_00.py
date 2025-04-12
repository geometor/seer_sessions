import numpy as np

"""
Processes a 1D input grid containing a single non-white pixel (red=2).
Generates a 2D output grid where the width and height are equal to the input width.
The first row of the output is a copy of the input.
Subsequent rows are generated based on a cellular automaton rule applied to the previous row:
- A cell becomes non-white if exactly one of its diagonal predecessors in the row above is non-white (XOR logic).
- If both diagonal predecessors are non-white (collision), the cell becomes white (0).
- If both diagonal predecessors are white, the cell remains white (0).
- The color of the generated non-white cell depends on the row index:
    - For rows 1 and 2 (indices 1 and 2), the color is red (2).
    - For rows 3 and onwards (indices > 2), the color is blue (1).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the described cellular automaton rules.

    Args:
        input_grid: A list containing a single list of integers (1D grid).

    Returns:
        A list of lists of integers representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)

    # Determine the width (W) from the input grid
    # Input is guaranteed to be 1 row, so shape[1] gives width
    if input_np.ndim == 1: # Handle case if input is truly 1D array
         W = input_np.shape[0]
         input_np = input_np.reshape(1, W) # Reshape to 2D (1 row)
    elif input_np.ndim == 2:
         W = input_np.shape[1]
         if input_np.shape[0] != 1:
              raise ValueError("Input grid should have only one row.")
    else:
         raise ValueError("Input grid has unexpected dimensions.")


    # Initialize the output grid of size W x W with zeros (white)
    output_grid = np.zeros((W, W), dtype=int)

    # Copy the input row (row 0) into the first row of the output grid
    output_grid[0, :] = input_np[0, :]

    # Iterate through the rows of the output grid, starting from the second row (index 1)
    for r in range(1, W):
        # Get the previous row from the output grid
        prev_row = output_grid[r-1, :]

        # Iterate through the columns of the current row
        for c in range(W):
            # Get the values of the diagonal predecessors (top-left and top-right)
            # Handle boundary conditions: treat out-of-bounds cells as white (0)
            L = prev_row[c-1] if c > 0 else 0
            R = prev_row[c+1] if c < W - 1 else 0

            # Apply the transformation rules based on predecessors L and R
            if L != 0 and R != 0:
                # Collision: Both predecessors are non-white, resulting cell is white
                output_grid[r, c] = 0
            elif L != 0 or R != 0:
                # Propagation: Exactly one predecessor is non-white (L XOR R is true)
                # Determine color based on the row index 'r'
                if r <= 2:
                    # For rows 1 and 2 (index 1 and 2), the color is red (2)
                    output_grid[r, c] = 2
                else:
                    # For rows 3 and onwards (index > 2), the color is blue (1)
                    output_grid[r, c] = 1
            else:
                # Both predecessors are white, resulting cell is white
                output_grid[r, c] = 0

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
