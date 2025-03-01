"""
The output grid is constructed by taking the unique colors of the input grid, and creating a 1 x N grid, where N is the number of unique colors. The values are placed in the output grid in the order that they *first appear* when reading the input grid from left to right, top to bottom. The output is a single row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the first appearance of unique colors.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed 1 x N grid.
    """
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)

    # Flatten the input array to read it left-to-right, top-to-bottom
    flattened_array = input_array.flatten()

    # Get unique elements, preserving order
    unique_elements = []
    for element in flattened_array:
        if element not in unique_elements:
            unique_elements.append(element)

    # Create the 1 x N output grid
    output_grid = [unique_elements]

    return output_grid