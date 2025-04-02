```python
import numpy as np

"""
The transformation identifies 2x2 regions in the input grid starting at coordinates (r, c) where both r and c are even.
If such a 2x2 region contains at least one pair of adjacent (horizontal or vertical) pixels of the same non-background color, 
then the corresponding 2x2 region in the output grid (at the same coordinates (r, c)) is filled entirely with that color. 
Otherwise, the 2x2 output region remains the background color (white, 0).
The output grid is initialized with the background color.
"""

def find_pair_color_in_2x2(subgrid: np.ndarray) -> int:
    """
    Checks a 2x2 subgrid for any adjacent pair of identical, non-background pixels.

    Args:
        subgrid: A 2x2 numpy array.

    Returns:
        The color of the first found pair, or 0 if no such pair is found.
    """
    # Check horizontal pair in top row
    if subgrid[0, 0] != 0 and subgrid[0, 0] == subgrid[0, 1]:
        return subgrid[0, 0]
    # Check horizontal pair in bottom row
    if subgrid[1, 0] != 0 and subgrid[1, 0] == subgrid[1, 1]:
        return subgrid[1, 0]
    # Check vertical pair in left column
    if subgrid[0, 0] != 0 and subgrid[0, 0] == subgrid[1, 0]:
        return subgrid[0, 0]
    # Check vertical pair in right column
    if subgrid[0, 1] != 0 and subgrid[0, 1] == subgrid[1, 1]:
        return subgrid[0, 1]
    # No non-background adjacent pair found
    return 0

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding adjacent pairs within 2x2 regions 
    starting at even coordinates and creating corresponding 2x2 colored squares in the output.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through potential top-left corners (r, c) of 2x2 blocks
    # where r and c are even
    for r in range(0, height - 1, 2):  # Stop before the last row if height is odd
        for c in range(0, width - 1, 2): # Stop before the last col if width is odd
            
            # Extract the 2x2 subgrid from the input
            input_subgrid = input_grid[r:r+2, c:c+2]

            # Check if this subgrid contains a qualifying adjacent pair
            pair_color = find_pair_color_in_2x2(input_subgrid)

            # If a pair was found (color is not 0)
            if pair_color != 0:
                # Fill the corresponding 2x2 region in the output grid with the pair's color
                output_grid[r:r+2, c:c+2] = pair_color

    return output_grid
```