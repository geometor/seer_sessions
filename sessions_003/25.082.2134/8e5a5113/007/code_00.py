"""
The input grid is divided into sections by separator columns of color 5 (gray). The leftmost section, before the first separator, is the "Left Section." The Left Section is copied to the output. The first separator is copied. The section between the first and second separators is a 180-degree rotated copy of the Left Section. The rightmost section is also a 180-degree rotated copy of the Left Section. If a second separator exists, it's copied. If no separators exist, output is same as input.
"""

import numpy as np

def get_left_section(grid):
    """Finds the first separator column and returns the grid up to the separator."""
    separator_col = np.where(grid[0,:] == 5)[0]
    if separator_col.size > 0:
        return grid[:, :separator_col[0]]
    else:
        return grid

def get_separator_columns(grid):
    """Finds all separator columns indices."""
    return np.where(grid[0,:] == 5)[0]

def mirror_section(grid):
    """Mirrors a section by reversing rows and columns (180-degree rotation)."""
    return np.rot90(grid, 2)

def transform(input_grid):
    # Initialize output_grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)
    input_grid = np.array(input_grid) # ensure numpy array

    # 1. Identify Separators
    separator_cols = get_separator_columns(input_grid)

    # 2. Handle No Separators
    if len(separator_cols) == 0:
        return input_grid

    # 3. Left Section
    left_section = get_left_section(input_grid)

    # 4. Copy Left Section
    output_grid[:, :left_section.shape[1]] = left_section

    # 5. Copy First Separator
    first_separator_col_index = separator_cols[0]
    output_grid[:, first_separator_col_index] = input_grid[:, first_separator_col_index]

    # 6. Middle Section (Mirrored)
    middle_section_start = first_separator_col_index + 1
    mirrored_left_section = mirror_section(left_section)

    if len(separator_cols) > 1:
        # Second separator exists
        second_separator_col_index = separator_cols[1]
        middle_section_end = second_separator_col_index
        output_grid[:, middle_section_start:middle_section_end] = mirrored_left_section[:, :middle_section_end-middle_section_start]

        # 8. Copy Second Separator
        output_grid[:, second_separator_col_index] = input_grid[:, second_separator_col_index]

        # 7. Right section
        right_section_start = second_separator_col_index + 1
        output_grid[:, right_section_start:] = mirrored_left_section[:, :output_grid.shape[1] - right_section_start]

    else:
        # No second separator
        middle_section_end = middle_section_start + mirrored_left_section.shape[1]

        # make sure not to write outside of the grid.
        middle_section_end = min(middle_section_end,output_grid.shape[1])

        output_grid[:, middle_section_start:middle_section_end] = mirrored_left_section[:,:middle_section_end-middle_section_start ]
      
        # 7. Right Section Start
        right_section_start = middle_section_end
        
        output_grid[:, right_section_start:] = mirrored_left_section[:,:output_grid.shape[1]-right_section_start]


    return output_grid