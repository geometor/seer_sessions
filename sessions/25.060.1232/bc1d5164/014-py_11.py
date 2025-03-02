"""
The transformation extracts a subgrid from the input grid. The subgrid's columns correspond to the columns in the input grid where unique colors first appear, considering only the last row of the input where non-black colors exist.  The output grid consists of the first, middle, and last of these columns. The output is then transposed.
"""

import numpy as np

def get_unique_color_columns_last_row(grid):
    """
    Finds the column indices where unique colors (excluding black) first appear
    in the last row that contains non-black colors.
    """
    rows, cols = grid.shape
    last_row_with_colors = None

    # Find the last row with non-black colors
    for i in reversed(range(rows)):
        if any(color != 0 for color in grid[i]):
            last_row_with_colors = grid[i]
            break

    if last_row_with_colors is None:
        return []

    unique_colors = set()
    column_indices = []

    # Iterate through the last row with colors
    for j, color in enumerate(last_row_with_colors):
        if color != 0 and color not in unique_colors:
            unique_colors.add(color)
            column_indices.append(j)

    return sorted(column_indices)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find columns with first occurrence of unique colors in last colored row
    unique_color_columns_indices = get_unique_color_columns_last_row(input_grid)
    
    # Handle cases where there are fewer than 3 unique color columns
    if len(unique_color_columns_indices) == 0:
        return []
    elif len(unique_color_columns_indices) == 1:
        selected_columns = [unique_color_columns_indices[0]] * 3
    elif len(unique_color_columns_indices) == 2:
      
        selected_columns = [unique_color_columns_indices[0], unique_color_columns_indices[0], unique_color_columns_indices[1]]

    else:
        # Find the relevant columns (first, middle, and last)
        first = unique_color_columns_indices[0]
        middle = unique_color_columns_indices[len(unique_color_columns_indices)//2]
        last = unique_color_columns_indices[-1]
        selected_columns = [first, middle, last]

    
    # Create the output grid
    output_grid = np.array([
      input_grid[:, col] for col in selected_columns
    ]).T


    return output_grid.tolist()