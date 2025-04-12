import numpy as np
from typing import List

"""
Transformation Rule:

The transformation depends on whether a 3x3 block of red (2) pixels exists in the input grid.

1. Check for 3x3 Red Block: Scan the input grid to find if any 3x3 area consists entirely of red (2) pixels.

2. Conditional Transformation:
   a. If a 3x3 red block IS found:
      i. Initialize the output grid as a copy of the input grid.
      ii. Identify the top-left coordinates of all 3x3 blocks in the *input* grid that consist entirely of blue (1) pixels.
      iii. Change all white (0) pixels in the output grid to blue (1).
      iv. For each identified 3x3 blue block location from step (ii), change the corresponding 3x3 area in the *output* grid to white (0).
   b. If a 3x3 red block IS NOT found:
      i. Initialize the output grid as a copy of the input grid.
      ii. Change all white (0) pixels in the output grid to blue (1).
      iii. Change all red (2) pixels in the output grid to white (0).

3. Return the modified output grid.
"""

def find_3x3_block(grid: np.ndarray, color: int) -> bool:
    """
    Checks if a 3x3 block of the specified color exists in the grid.

    Args:
        grid: The input grid as a NumPy array.
        color: The color to search for (integer 0-9).

    Returns:
        True if a 3x3 block of the specified color is found, False otherwise.
    """
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            if np.all(subgrid == color):
                return True
    return False

def find_all_3x3_block_coords(grid: np.ndarray, color: int) -> List[tuple[int, int]]:
    """
    Finds the top-left coordinates of all 3x3 blocks of the specified color.

    Args:
        grid: The input grid as a NumPy array.
        color: The color to search for.

    Returns:
        A list of (row, col) tuples representing the top-left corners.
    """
    coords = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            if np.all(subgrid == color):
                coords.append((r, c))
    return coords

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the presence of a 3x3 red block.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Check if a 3x3 block of red (2) exists
    has_red_3x3 = find_3x3_block(input_array, 2)

    if has_red_3x3:
        # Branch 1: 3x3 red block exists
        
        # Find locations of original 3x3 blue blocks first
        blue_3x3_coords = find_all_3x3_block_coords(input_array, 1)

        # Change white (0) to blue (1) in the output
        output_array[input_array == 0] = 1
        
        # Change original 3x3 blue blocks to white (0) in the output
        for r, c in blue_3x3_coords:
            output_array[r:r+3, c:c+3] = 0
            
    else:
        # Branch 2: No 3x3 red block exists
        
        # Change white (0) to blue (1)
        output_array[input_array == 0] = 1
        
        # Change red (2) to white (0)
        output_array[input_array == 2] = 0

    # Convert back to list of lists and return
    return output_array.tolist()