"""
Selects columns from the input grid to create the output grid. The selection
is based on the most frequent color in each column, matching the most frequent
color in the entire input grid.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Determine the most frequent color in the entire input grid.
    all_colors = []
    for i in range(rows):
      for j in range(cols):
        all_colors.append(input_grid[i,j])
        
    most_frequent_color = Counter(all_colors).most_common(1)[0][0]

    # Find columns where the most frequent color matches the overall most frequent color.
    selected_columns = []
    for j in range(cols):
        column_colors = input_grid[:, j]
        most_frequent_in_column = Counter(column_colors).most_common(1)[0][0]
        if most_frequent_in_column == most_frequent_color:
            selected_columns.append(j)

    # Create the output grid.
    output_width = len(selected_columns)
    output_grid = np.empty((rows, output_width), dtype=int)

    # Copy the selected columns to the output grid.
    for i, col_index in enumerate(selected_columns):
        output_grid[:, i] = input_grid[:, col_index]

    return output_grid.tolist()