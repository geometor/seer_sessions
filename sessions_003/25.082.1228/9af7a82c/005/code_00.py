"""
1.  **Input:** Receive the input grid as a 2D array of integers (colors).
2.  **Unique Colors:** Identify all unique color values present in the input grid.
3.  **Sort Colors:** Sort the unique colors in ascending order.
4.  **Output Dimensions:**
    *   Output Width: The number of unique colors.
    *   Output Height: The maximum number of times any single color appears anywhere in the input grid.
5.  **Create Output Grid:** Initialize an output grid filled with zeros, with the calculated dimensions.
6.  **Populate Columns:**
      * Iterate through each sorted unique color. This color will be the "target color" for the current column.
      * Iterate through input grid, looking for instances of target color.
      * For each instance of target color, add it to the next available spot on the output grid for that color.
7.  **Return:** Return the completed output grid.
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

    # Extract unique values and sort them in ascending order
    unique_values = np.unique(input_array)
    sorted_values = np.sort(unique_values)

    # Determine output grid dimensions
    output_height = get_max_color_count(input_grid)
    output_width = len(sorted_values)

    # Create an output grid of size output_height x output_width, filled with 0s
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate the output grid with the sorted values
    column_indices = {}  # Keep track of the next row index for each color
    for col_index, value in enumerate(sorted_values):
        column_indices[value] = 0

    for i in range(input_array.shape[0]):  # Iterate through each row of input
        for j in range(input_array.shape[1]):  # Iterate through each column of input
            current_color = input_array[i,j]
            if current_color in sorted_values:
                row_index = column_indices[current_color]
                col_index = np.where(sorted_values == current_color)[0][0]  # Find column index
                if row_index < output_height:
                   output_grid[row_index, col_index] = current_color
                   column_indices[current_color] += 1

    return output_grid.tolist()