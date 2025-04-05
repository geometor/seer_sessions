```python
import numpy as np

def transform(input_grid):
    """
    Transforms a 2D grid based on the following rule:
    A cell containing 0 is changed to 8 if it lies directly between two 8s,
    either horizontally or vertically. Cells originally containing 8 remain unchanged.
    Cells containing 0 that do not meet the condition also remain unchanged.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)

    # Get the dimensions of the grid
    height, width = input_array.shape

    # Iterate through each cell of the input grid, excluding the borders
    # Border cells cannot be 'between' two neighbors within the grid
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current cell in the input grid is 0
            if input_array[r, c] == 0:
                # Check vertical neighbors: if the cell above and below are both 8
                is_between_vertical = (input_array[r - 1, c] == 8 and input_array[r + 1, c] == 8)
                
                # Check horizontal neighbors: if the cell to the left and right are both 8
                is_between_horizontal = (input_array[r, c - 1] == 8 and input_array[r, c + 1] == 8)

                # If the cell is 0 and is between two 8s either vertically or horizontally
                if is_between_vertical or is_between_horizontal:
                    # Update the corresponding cell in the output grid to 8
                    output_array[r, c] = 8

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid

```