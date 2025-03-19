"""
1. **Identify Unique Colors:** Extract the first row of the input grid. Find the unique, non-zero values in this row. These values represent the colors that will be used in the output grid.
2. **Determine Output Dimensions:** The output grid will have the same number of rows as the input grid. The number of columns in the output grid will be equal to the number of unique, non-zero colors found in the input's first row.
3. **Color Mapping:** Create the output grid. For each column in the output, use the corresponding unique color from the input's first row. If the color is 1, change to color 8.
4. Fill Columns: Fill each column with the mapped color.
5. **Return Output:** The output grid.
"""

import numpy as np

def transform(input_grid):
    # Get the first row of the input grid
    first_row = input_grid[0]

    # Find the unique non-zero values in the first row
    unique_colors = np.unique(first_row[first_row != 0])

    # Determine the dimensions of the output grid
    rows = len(input_grid)
    cols = len(unique_colors)

    # Initialize the output grid with zeros
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through the unique colors and fill the output grid
    for i, color in enumerate(unique_colors):
        # Map color 1 to color 8
        if color == 1:
            mapped_color = 8
        else:
            mapped_color = color

        # Fill the corresponding column with the mapped color
        output_grid[:, i] = mapped_color

    return output_grid