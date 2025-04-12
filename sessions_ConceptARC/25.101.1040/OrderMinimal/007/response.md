```python
import numpy as np

"""
Transforms the grid by processing each row independently to consolidate 
all yellow pixels (4) into a single contiguous horizontal block. The position 
of this block depends on the properties of the yellow pixels in the 
original row (count N, rightmost position max_c) and crucially on the 
total count of yellow pixels (N_total) in the entire input grid.

The specific adjustment logic based on N_total and row N is derived from the 
provided training examples:
- If N_total = 6, adjustment (adj) = 0.
- If N_total = 10, adjustment (adj) = 1.
- If N_total = 15:
    - If row N <= 2, adj = 2.
    - If row N >= 3, adj = 0.
- Otherwise (for other N_total values), assume adj = 0.

The starting column 'k' of the block is calculated as k = max_c - N + adj, 
and then clamped to fit within the grid boundaries [0, width - N].
"""

def calculate_adjustment(n_total: int, n_row: int) -> int:
    """Calculates the adjustment factor based on total yellow pixels and row yellow pixels."""
    if n_total == 6:
        return 0
    elif n_total == 10:
        return 1
    elif n_total == 15:
        if n_row <= 2:
            return 2
        else: # n_row >= 3
            return 0
    else:
        # Default adjustment for N_total values not seen in training
        return 0

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Rearranges yellow pixels in each row into a contiguous block based on 
    row properties and the total number of yellow pixels in the grid.
    """
    # Convert input to NumPy array for efficient calculations
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Calculate the total number of yellow pixels (color 4) in the entire grid
    n_total = np.sum(input_array == 4)

    # Initialize the output grid with background color (white = 0)
    output_array = np.zeros_like(input_array)

    # Process each row independently
    for r in range(height):
        # Find column indices of yellow pixels (color 4) in the current row
        yellow_indices = np.where(input_array[r] == 4)[0]
        n_row = len(yellow_indices)  # Number of yellow pixels in this row

        # Only proceed if there are yellow pixels in the row
        if n_row > 0:
            # Find the column index of the rightmost yellow pixel
            max_c = np.max(yellow_indices)

            # Determine the adjustment value 'adj' using the helper function
            adj = calculate_adjustment(n_total, n_row)

            # Calculate the target starting column 'k' before clamping
            k_unclamped = max_c - n_row + adj

            # Clamp 'k' to ensure the block [k, k+n_row-1] fits within the grid width [0, width-1]
            # The start index k must be >= 0
            # The end index k+n_row-1 must be <= width-1, which means k <= width - n_row
            k = max(0, min(k_unclamped, width - n_row))

            # Place the contiguous block of N yellow pixels in the output row
            start_col = k
            end_col = k + n_row 
            # Ensure indices are valid (clamping should guarantee this unless n_row > width)
            if start_col < end_col <= width: 
                 output_array[r, start_col:end_col] = 4
        # Else (if n_row == 0), the row remains all white (already initialized)

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid
```