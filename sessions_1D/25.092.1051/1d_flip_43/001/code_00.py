import numpy as np
from typing import List, Tuple

"""
Transforms a 1D input grid (single row) by swapping the positions of an adjacent single non-white pixel and a contiguous block of non-white pixels of a different color.

Specifically:
1. Finds the first non-white pixel (color_A at index_A).
2. Finds the adjacent contiguous block of a different non-white color (color_B starting at index_B with length_B).
3. In the output grid, places the block (color_B) starting at index_A.
4. Places the single pixel (color_A) immediately after the block, at index_A + length_B.
5. Keeps all other pixels (background white) unchanged.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Swaps an adjacent single pixel and a block in a 1D grid.

    Args:
        input_grid: A list containing a single list of integers representing the input row.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    # Ensure input is a single row grid
    if len(input_grid) != 1:
        # Handle error or unexpected input format if necessary
        # For now, assume valid input as per examples
        return input_grid 
        
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy
    grid_width = len(input_row)

    # Initialize variables to store properties of the elements
    color_A = -1
    index_A = -1
    color_B = -1
    index_B = -1
    length_B = 0

    # 1. Find the single pixel (color_A, index_A)
    for i in range(grid_width):
        if input_row[i] != 0:
            color_A = input_row[i]
            index_A = i
            break # Found the first non-white pixel

    # Check if a non-white pixel was found
    if index_A == -1:
        # No non-white pixels found, return original grid
        return input_grid

    # 2. Find the adjacent block (color_B, index_B, length_B)
    # Block must start immediately after the single pixel
    index_B = index_A + 1
    if index_B < grid_width and input_row[index_B] != 0 and input_row[index_B] != color_A:
        color_B = input_row[index_B]
        # Calculate the length of the block
        current_index = index_B
        while current_index < grid_width and input_row[current_index] == color_B:
            length_B += 1
            current_index += 1
    
    # Check if a valid adjacent block was found
    if length_B == 0:
        # No valid adjacent block found, return original grid
        # This scenario might indicate an edge case or invalid input structure according to the pattern
        return input_grid

    # 3. & 4. Modify the output grid: Place block at index_A, place single pixel at index_A + length_B
    # Place the block
    for j in range(length_B):
        # Check bounds just in case, though based on logic it should fit
        if index_A + j < grid_width:
            output_row[index_A + j] = color_B
        
    # Place the single pixel
    # Check bounds
    if index_A + length_B < grid_width:
       output_row[index_A + length_B] = color_A

    # 5. Return the modified output grid (wrapped in a list)
    return [output_row]
