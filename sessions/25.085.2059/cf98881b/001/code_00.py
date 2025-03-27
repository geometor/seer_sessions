"""
The transformation rule involves identifying three 4x4 sections in the 4x14 input grid, defined by fixed vertical red delimiters at column indices 4 and 9. The output is a 4x4 grid created by overlaying these three sections with a specific priority. For each cell (r, c) in the output:
1. Use the color from Section 1 (cols 0-3) at (r, c) if it's not white (0).
2. Otherwise, use the color from Section 2 (cols 5-8) at (r, c) if it's not white (0).
3. Otherwise, use the color from Section 3 (cols 10-13) at (r, c).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the prioritized overlay transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 4x4 numpy array representing the transformed output grid.
    """
    
    # Assume input dimensions are always 4x14 and output is 4x4
    output_height = 4
    output_width = 4

    # Extract the three relevant 4x4 sections from the input grid
    # Section 1: Columns 0-3
    section1 = input_grid[0:output_height, 0:output_width]
    
    # Section 2: Columns 5-8 (skipping delimiter at col 4)
    section2 = input_grid[0:output_height, 5:5+output_width]
    
    # Section 3: Columns 10-13 (skipping delimiter at col 9)
    section3 = input_grid[0:output_height, 10:10+output_width]

    # Initialize the output grid (e.g., with zeros or copy section3 as base)
    # Let's initialize with zeros for clarity
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell position in the 4x4 grid
    for r in range(output_height):
        for c in range(output_width):
            # Get the colors from the corresponding positions in each section
            color1 = section1[r, c]
            color2 = section2[r, c]
            color3 = section3[r, c]

            # Apply the priority logic
            if color1 != 0:  # Check Section 1 first (non-white)
                output_grid[r, c] = color1
            elif color2 != 0: # Check Section 2 second (non-white)
                output_grid[r, c] = color2
            else: # Otherwise, use Section 3's color
                output_grid[r, c] = color3

    return output_grid
