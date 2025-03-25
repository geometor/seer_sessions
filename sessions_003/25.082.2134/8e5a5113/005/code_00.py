"""
The input grid is divided into sections by columns of 5s. The Left Section is copied to the output. The first separator column is copied to the output. The section immediately to the right of separator, mirrors the Left Section (reversing both rows and columns, equivalent to a 180-degree rotation). The final section (right-most) of output also mirrors a flipped version of left section. The second separator column is copied. Dimensions of the sections are determined dynamically.
"""

import numpy as np

def get_left_section(grid):
    """Finds the first separator column and returns the grid up to the separator."""
    separator_col = np.where(grid[0,:] == 5)[0]
    # Handle the case where there's no separator
    if separator_col.size > 0:
        return grid[:, :separator_col[0]]
    else:
        return grid  # Or return None, or raise an exception, depending on desired behavior

def get_separator_columns(grid):
    """Finds all separator columns indices"""
    separator_cols = np.where(grid[0,:] == 5)[0]
    return separator_cols

def mirror_section(grid):
    """Mirrors a section by reversing rows and columns (180-degree rotation)."""
    return np.rot90(grid, 2)

def transform(input_grid):
    # Initialize output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Get the left section
    left_section = get_left_section(input_grid)

    # Get separator column indices
    separator_cols = get_separator_columns(input_grid)
    if len(separator_cols) == 0:
        return input_grid # if no separator return the original
    first_separator_col_index = separator_cols[0]
    
    second_separator_exists =  len(separator_cols) > 1
    if second_separator_exists:
      second_separator_col_index = separator_cols[1]


    # 1. Copy left section to output
    output_grid[:, :left_section.shape[1]] = left_section

    # 2. Copy First Separator Column
    output_grid[:, first_separator_col_index] = input_grid[:, first_separator_col_index]

    # 3. Mirror and copy to the middle section
    mirrored_left_section = mirror_section(left_section)
    middle_section_start = first_separator_col_index + 1
    middle_section_end = middle_section_start + mirrored_left_section.shape[1]
    
    if second_separator_exists:
      # if a second separator, make sure not to overwrite it
      middle_section_end = min(middle_section_end, second_separator_col_index)

    output_grid[:, middle_section_start:middle_section_end] = mirrored_left_section[:, :middle_section_end-middle_section_start]


    #4 mirror and copy to the last section
    right_section_start = output_grid.shape[1] - mirrored_left_section.shape[1]
    output_grid[:, right_section_start:] = mirrored_left_section
    
    #5 Copy second separator
    if second_separator_exists:
      output_grid[:, second_separator_col_index] = input_grid[:, second_separator_col_index]


    return output_grid