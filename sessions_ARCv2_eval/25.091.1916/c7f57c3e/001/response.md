```python
import numpy as np

"""
Transformation Rule based on train_1:

Iterate through each pixel of the input grid, except for the last row. 
For each pixel, determine its color and the color of the pixel directly below it. 
Apply the following rules in order to determine the output color for the current pixel:

1.  Initialize the output grid as a copy of the input grid.
2.  For each pixel (r, c) where r is less than the last row index:
    a. Get the `current_color` at `input_grid[r, c]`.
    b. Get the `below_color` at `input_grid[r+1, c]`.
    c. **Exception Rule:** If `current_color` is Red (2) AND it has a Blue (1) pixel immediately to its left (c > 0 and input_grid[r, c-1] == 1) AND a Blue (1) pixel immediately to its right (c < width-1 and input_grid[r, c+1] == 1), then this pixel does NOT change. Continue to the next pixel.
    d. **Rule 1:** If `current_color` is Azure (8) AND `below_color` is Azure (8), change the corresponding pixel in the output grid to Red (2).
    e. **Rule 2:** If `current_color` is Azure (8) AND `below_color` is Yellow (4), change the corresponding pixel in the output grid to Green (3).
    f. **Rule 3:** If `current_color` is Red (2) AND `below_color` is Green (3), change the corresponding pixel in the output grid to Azure (8). (This rule is skipped if the Exception Rule applied).
    g. **Rule 4:** If `current_color` is Green (3) AND (`below_color` is Yellow (4) OR `below_color` is Green (3)), change the corresponding pixel in the output grid to Azure (8).
3.  Pixels not matching any change condition, pixels affected by the exception rule, and pixels in the last row retain their original color from the input grid.
4.  Return the modified grid.
"""

def transform(input_grid):
    """
    Applies a transformation rule to the input grid based on the color of a pixel 
    and the color of the pixel directly below it, with specific exceptions.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for efficient element access
    grid = np.array(input_grid, dtype=int)
    # Create a copy of the grid to store the output, ensuring the input remains unchanged
    output_grid = grid.copy()
    # Get the dimensions (height, width) of the grid
    height, width = grid.shape

    # Iterate through each row except the last one
    for r in range(height - 1):
        # Iterate through each column in the current row
        for c in range(width):
            # Get the color of the current pixel
            current_color = grid[r, c]
            # Get the color of the pixel directly below the current one
            below_color = grid[r + 1, c]

            # Check for the specific exception: Red(2) flanked by Blue(1)
            if current_color == 2:
                # Ensure we are not on the left or right edge before checking neighbors
                if 0 < c < width - 1:
                    # Check if left and right neighbors are Blue(1)
                    if grid[r, c - 1] == 1 and grid[r, c + 1] == 1:
                        # If the exception condition is met, skip any transformation for this pixel
                        continue  

            # Apply transformation rules if the exception did not apply
            
            # Rule 1: Azure(8) transformations
            if current_color == 8:
                if below_color == 8:
                    output_grid[r, c] = 2  # Change to Red(2)
                elif below_color == 4:
                    output_grid[r, c] = 3  # Change to Green(3)
            
            # Rule 3: Red(2) transformation (only if exception didn't apply)
            elif current_color == 2:
                if below_color == 3:
                    output_grid[r, c] = 8  # Change to Azure(8)

            # Rule 4: Green(3) transformations
            elif current_color == 3:
                if below_color == 4 or below_color == 3:
                    output_grid[r, c] = 8  # Change to Azure(8)

    # Convert the final NumPy array back to a list of lists format
    return output_grid.tolist()
```