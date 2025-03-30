```python
import numpy as np

"""
Create a 15x15 output grid filled with orange (7).
Extract the central pattern from the input grid by removing the 1-pixel border.
Copy this extracted pattern onto the output grid twice:
1. Starting at row 2, column 2.
2. Starting at row 8, column 8.
"""

def transform(input_grid):
    """
    Transforms the input grid by extracting the core pattern (removing the border)
    and placing it twice onto a 15x15 orange background at fixed locations.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed 15x15 output grid.
    """
    # Convert input grid to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    input_h, input_w = input_np.shape

    # Define output grid dimensions and background color
    output_h = 15
    output_w = 15
    background_color = 7

    # Initialize the output grid with the background color
    output_grid = np.full((output_h, output_w), background_color, dtype=int)

    # Extract the core pattern by removing the 1-pixel border
    # Slicing [1:-1] removes the first and last row/column
    core_pattern = input_np[1:-1, 1:-1]
    core_h, core_w = core_pattern.shape

    # Define placement locations (0-indexed)
    loc1_r, loc1_c = 2, 2
    loc2_r, loc2_c = 8, 8

    # Copy the core pattern to the first location
    # Ensure the pattern fits within the bounds, though fixed size guarantees this here
    if loc1_r + core_h <= output_h and loc1_c + core_w <= output_w:
        output_grid[loc1_r:loc1_r + core_h, loc1_c:loc1_c + core_w] = core_pattern

    # Copy the core pattern to the second location
    if loc2_r + core_h <= output_h and loc2_c + core_w <= output_w:
        output_grid[loc2_r:loc2_r + core_h, loc2_c:loc2_c + core_w] = core_pattern

    return output_grid.tolist() # Return as list of lists if required by framework

```