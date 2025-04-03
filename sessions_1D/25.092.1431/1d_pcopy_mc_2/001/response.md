```python
import numpy as np

"""
Transformation Rule:
1. Identify non-white (non-zero) pixels in the 1D input grid.
2. Check if a non-white pixel is "isolated" horizontally, meaning its immediate left and right neighbors in the input grid are both white (zero). Boundary pixels (first and last) cannot be isolated in this way as they lack one neighbor.
3. If a non-white pixel at index `i` is isolated, expand it in the output grid by changing the pixels at indices `i-1` and `i+1` to the same color as the pixel at index `i`.
4. All other pixels (white pixels, non-white pixels that are not isolated, boundary pixels) retain their original color in the output grid.
"""

# No external libraries needed beyond standard list operations or numpy if preferred for array handling.
# Using standard lists for simplicity as the grid is 1D.

def transform(input_grid):
    """
    Expands isolated non-white pixels in a 1D grid into horizontal lines of three.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid.
    """
    # Get the width of the grid
    width = len(input_grid)
    
    # Initialize the output grid as a copy of the input grid.
    # This handles all pixels that don't need changing.
    output_grid = list(input_grid) 

    # Iterate through the input grid pixels, excluding the boundaries
    # as boundary pixels cannot be horizontally isolated according to the rule.
    for i in range(1, width - 1):
        # Get the color of the current pixel in the input grid
        current_color = input_grid[i]

        # Check if the current pixel is non-white (not 0)
        if current_color != 0:
            # Check if its immediate neighbors in the *input* grid are white (0)
            left_neighbor_color = input_grid[i - 1]
            right_neighbor_color = input_grid[i + 1]

            if left_neighbor_color == 0 and right_neighbor_color == 0:
                # If it's an isolated non-white pixel, expand it in the output grid
                # The center pixel output_grid[i] is already correct due to the initial copy.
                output_grid[i - 1] = current_color
                output_grid[i + 1] = current_color
                
    # Return the modified output grid
    return output_grid

```