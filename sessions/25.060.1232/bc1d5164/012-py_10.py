"""
The transformation extracts a subgrid from the input grid. The subgrid is formed by selecting the columns of the input grid where the first occurrences of unique colors (excluding black and white) appear.  It takes the first, middle, and last of these columns, then transposes the resulting subgrid.
"""

import numpy as np

def get_unique_color_columns(grid):
    """
    Finds the column indices of the first occurrence of each unique color (excluding 0 and 9) in the grid.
    """
    unique_colors = set()
    column_indices = []
    rows, cols = grid.shape

    for j in range(cols):
        for i in range(rows):
            color = grid[i][j]
            if color != 0 and color not in unique_colors:
                unique_colors.add(color)
                column_indices.append(j)
                break  # Move to the next column after finding a new unique color
    return sorted(column_indices)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find columns with first occurrence of unique colors
    unique_color_columns_indices = get_unique_color_columns(input_grid)
    
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