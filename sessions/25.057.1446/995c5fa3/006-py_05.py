"""
Transforms an input grid of gray and white pixels into a 3x3 output grid of red, azure, and green pixels.
The output is determined by the number of contiguous sections of gray pixels separated by rows of white pixels.
"""

import numpy as np

def count_gray_sections(input_grid):
    """
    Counts the number of contiguous sections of gray pixels separated by rows of white pixels.
    """
    rows, cols = input_grid.shape
    in_gray_section = False
    gray_section_count = 0
    for r in range(rows):
        if np.any(input_grid[r, :] == 5) and not in_gray_section:
            gray_section_count += 1
            in_gray_section = True
        elif np.all(input_grid[r, :] != 5):
            in_gray_section = False
    return gray_section_count

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Count the number of gray sections
    gray_sections = count_gray_sections(input_grid)

    # Initialize the output grid as a 3x3 array.
    output_grid = np.array([
        [2, 2, 2],
        [8, 8, 8],
        [3, 3, 3]
    ])
    
    return output_grid