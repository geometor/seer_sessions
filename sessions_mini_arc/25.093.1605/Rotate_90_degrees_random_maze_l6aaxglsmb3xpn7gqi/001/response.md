```python
import numpy as np

def transform(input_grid):
    """
    Rotates the input 5x5 grid 90 degrees clockwise.

    1. Initialize an empty 5x5 output grid, filling all cells with the value 0.
    2. Examine each cell of the input grid, identifying its row index `r` and column index `c` (from 0 to 4).
    3. Retrieve the value `v` located at the input cell (`r`, `c`).
    4. If the value `v` is not 0:
       a. Calculate the corresponding output coordinates (`r'`, `c'`) based on a 90-degree clockwise rotation: `r'` is the original column `c`, and `c'` is `4 - r` (where 4 is the maximum index for a 5x5 grid).
       b. Assign the value `v` to the output grid cell at the calculated coordinates (`r'`, `c'`).
    5. After processing all cells from the input grid, the populated output grid represents the final result.
    """

    # Convert input list of lists to a NumPy array for easier handling
    input_array = np.array(input_grid)
    
    # Get the dimensions of the grid (assuming square)
    n = input_array.shape[0]
    
    # Initialize an output grid of the same size, filled with zeros
    output_array = np.zeros_like(input_array)

    # Iterate through each cell of the input grid
    for r in range(n):
        for c in range(n):
            # Get the value from the input cell
            value = input_array[r, c]
            
            # If the value is non-zero, calculate its new position and place it
            if value != 0:
                # Calculate new coordinates for 90-degree clockwise rotation
                # New row `r'` becomes the original column `c`
                # New column `c'` becomes `n - 1 - r` (e.g., 4 - r for a 5x5 grid)
                new_r = c
                new_c = n - 1 - r
                
                # Assign the value to the corresponding cell in the output grid
                output_array[new_r, new_c] = value

    # Convert the output NumPy array back to a list of lists for the required format
    output_grid = output_array.tolist()
    
    return output_grid
```