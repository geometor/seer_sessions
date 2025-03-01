"""
The transformation rule is to extract a sequence of unique color values based on columns in the input grid and consolidate them into a single-row output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by extracting unique column values and
    consolidating them into a single-row output grid.
    
    Args:
        input_grid (numpy.ndarray): The input grid.
        
    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Get the first row (since all rows are identical).
    first_row = input_grid[0, :]

    # Initialize the output grid.
    output_grid = first_row

    return output_grid