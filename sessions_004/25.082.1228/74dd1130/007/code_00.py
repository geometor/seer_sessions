"""
Rearranges the elements within each column of a 3x3 grid independently.
The rearrangement sorts each column, giving precedence to the color that appears most frequently at the top of the column.
"""

import numpy as np

def transform(input_grid):
    """
    Rearranges each column of the input grid based on color frequency and top position.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the output grid, with each column rearranged.
    """
    input_array = np.array(input_grid)
    output_array = np.empty_like(input_array)

    for j in range(input_array.shape[1]):
        column = input_array[:, j]
        unique_colors, counts = np.unique(column, return_counts=True)
        
        # Sort colors by count, with original position as tie-breaker
        #argsort gives indices that would sort the array
        sorted_indices = np.lexsort((np.argsort(column), -counts)) #sort by counts descending, then original order
        sorted_colors = unique_colors[sorted_indices]

        # Build the sorted column
        sorted_column = []
        for color in sorted_colors:
            sorted_column.extend([color] * counts[np.where(unique_colors == color)[0][0]])

        output_array[:, j] = sorted_column

    output_grid = output_array.tolist()
    return output_grid