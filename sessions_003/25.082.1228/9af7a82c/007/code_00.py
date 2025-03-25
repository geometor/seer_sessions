"""
1.  **Input:** The input is a grid (2D array) of integers, where each integer represents a color.
2.  **Identify Unique Colors:** Find all the unique color values present in the input grid.
3.  **Sort Unique Colors:** Sort the unique colors in ascending order.
4.  **Determine Output Dimensions:**
    *   The width of the output grid is equal to the number of unique colors.
    *   The height of the output grid is equal to the maximum number of times any single color appears in the input grid.
5.  **Create Output Grid:** Initialize an output grid filled with zeros, with the calculated dimensions (height and width).
6.  **Populate Output Grid Columns:**
    *   Iterate through each unique color in the sorted list.
    *   For each unique color:
        *   Iterate through *all* cells of the input grid.
        *   If a cell in the input grid matches the current unique color, place the color value in the next available row of the corresponding column in the output grid. The column index corresponds to the position of that unique color in the sorted unique colors list.
        *   continue until all cells of that color have been added
7.  **Output:** Return the populated output grid.
"""

import numpy as np

def get_max_color_count(grid):
    """Calculates the maximum count of any single color in the grid."""
    input_array = np.array(grid)
    unique_values = np.unique(input_array)
    max_count = 0
    for value in unique_values:
        count = np.sum(input_array == value)
        max_count = max(max_count, count)
    return max_count

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Identify and sort unique colors
    unique_values = np.unique(input_array)
    sorted_values = np.sort(unique_values)

    # Determine output grid dimensions
    output_height = get_max_color_count(input_grid)
    output_width = len(sorted_values)

    # Create an output grid filled with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid, column by column
    column_indices = {}  # Track the next available row for each color
    for col_index, color in enumerate(sorted_values):
        column_indices[color] = 0  # Initialize row index for the current color
        for row_index in range(input_array.shape[0]):
            for cell_index in range(input_array.shape[1]):
                if input_array[row_index, cell_index] == color:
                    output_row = column_indices[color]
                    if output_row < output_height:  # important! make sure we do not add beyond bounds
                        output_grid[output_row, col_index] = color
                        column_indices[color] += 1


    return output_grid.tolist()