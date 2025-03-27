```python
"""
Transforms an input grid into an output grid by extracting colored regions above and below a horizontal azure line, and then stacking these regions.
"""

import numpy as np

def get_azure_line_row(grid):
    """Finds the row index of the horizontal azure line."""
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1  # Should not happen given the task description

def extract_colored_columns(grid_section):
    """
    Extracts colored (non-white, non-azure) pixel regions column-wise,
    preserving relative row indices within the section.
    Returns a list of lists, where each sublist represents a column
    and contains tuples: (row_index, pixel_value).
    """
    num_rows, num_cols = grid_section.shape
    colored_columns = []

    for j in range(num_cols):
        col_data = []
        for i in range(num_rows):
            pixel = grid_section[i, j]
            if pixel != 0 and pixel != 8:
                col_data.append((i, pixel))  # Store row index and pixel value
        if col_data:
            colored_columns.append(col_data)
    return colored_columns

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    input_grid = np.array(input_grid)
    azure_line_row = get_azure_line_row(input_grid)

    # Separate the grid into sections above and below the azure line
    top_section = input_grid[:azure_line_row]
    bottom_section = input_grid[azure_line_row + 1:]

    # Extract colored columns from each section, preserving row indices
    top_colored_columns = extract_colored_columns(top_section)
    bottom_colored_columns = extract_colored_columns(bottom_section)
    
    #find bounding box of top section
    top_rows = 0
    if len(top_colored_columns) > 0:
        top_rows = max(item[0] for sublist in top_colored_columns for item in sublist) + 1
    top_cols = len(top_colored_columns)

    #find bounding box of bottom section
    bottom_rows = 0
    if len(bottom_colored_columns) > 0:
        bottom_rows = max(item[0] for sublist in bottom_colored_columns for item in sublist) + 1
    bottom_cols = len(bottom_colored_columns)

    output_height = top_rows + bottom_rows
    output_width = max(top_cols, bottom_cols)

    if output_height > 0 and output_width > 0:
      output_grid = np.zeros((output_height, output_width), dtype=int)
    else:
      return []

    # Populate the output grid using the extracted column data
    for j, col in enumerate(top_colored_columns):
        for row_index, pixel_value in col:
            output_grid[row_index, j] = pixel_value

    for j, col in enumerate(bottom_colored_columns):
        for row_index, pixel_value in col:
            output_grid[row_index + top_rows, j] = pixel_value  # Offset by top_rows


    return output_grid.tolist()
```