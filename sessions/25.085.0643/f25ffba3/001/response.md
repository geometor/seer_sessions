```python
import numpy as np

"""
This program transforms an input grid based on the following rules:
1. Determine the height (H) and width (W) of the input grid.
2. Calculate the midpoint row index M = H / 2.
3. Create a new output grid with the same dimensions (H x W).
4. Identify the subgrid corresponding to the bottom half of the input grid (rows M to H-1).
5. Copy this bottom-half subgrid directly to the bottom half of the output grid (rows M to H-1).
6. Create a vertically flipped version of the bottom-half subgrid from the input.
7. Copy this flipped subgrid to the top half of the output grid (rows 0 to M-1).
8. Return the completed output grid.
The resulting output grid exhibits vertical symmetry across its horizontal midpoint.
"""

def transform(input_grid):
    """
    Transforms the input grid by copying its bottom half to the output's bottom half,
    and copying a vertically flipped version of the input's bottom half to the output's top half.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get grid dimensions
    height, width = input_np.shape

    # Calculate the midpoint row index (integer division)
    midpoint = height // 2

    # Initialize the output grid as a numpy array of the same shape, filled with zeros initially
    output_np = np.zeros_like(input_np)

    # Extract the bottom half of the input grid
    bottom_half_input = input_np[midpoint:, :]

    # Copy the bottom half of the input to the bottom half of the output
    output_np[midpoint:, :] = bottom_half_input

    # Flip the extracted bottom half vertically
    flipped_bottom_half = np.flipud(bottom_half_input)

    # Copy the flipped bottom half to the top half of the output
    output_np[:midpoint, :] = flipped_bottom_half

    # Convert the output numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid

```