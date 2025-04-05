```python
import numpy as np
from typing import List

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms an N x N input grid based on the following rules:
    1. Rows 2 through N from the input grid are copied into rows 1 through N-1 of the output grid.
    2. The Nth (last) row of the output grid is constructed as follows:
       - The first element (column 1) is the value from the input grid's first row, last column (row 1, column N).
       - All subsequent elements (columns 2 through N) are set to 0.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid)
    n_rows, n_cols = input_array.shape

    # Ensure the grid is square (though examples are all 5x5)
    if n_rows != n_cols:
        raise ValueError("Input grid must be square (N x N)")
    
    N = n_rows

    # Initialize the output grid (e.g., with zeros)
    # Using numpy makes initialization and slicing easier
    output_array = np.zeros_like(input_array)

    # Step 3: Copy rows 2 through N from input to rows 1 through N-1 of output
    # Input rows are indexed 1 to N-1 (Python slicing input_array[1:N])
    # Output rows are indexed 0 to N-2 (Python slicing output_array[0:N-1])
    output_array[0:N-1, :] = input_array[1:N, :]

    # Step 4: Extract the value from row 1, column N of the input grid
    # Input row 1 is index 0, column N is index N-1
    extracted_value = input_array[0, N-1]

    # Step 5: Construct the Nth (last) row of the output grid
    # Output row N is index N-1
    # Set the first element (column 1, index 0) to the extracted value
    output_array[N-1, 0] = extracted_value
    # The rest of the row is already initialized to 0 by np.zeros_like

    # Convert the result back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```