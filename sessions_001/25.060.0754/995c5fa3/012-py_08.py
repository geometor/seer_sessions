"""
Divides the input grid into nine equal sections.
For each section, it checks if all pixels are 0.
The output grid's corresponding cell value is based on pre-defined mapping.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Define section boundaries dynamically
    section_width = input_width // 3
    section_height = input_height // 3

    # Define output mapping: section_index -> color
    output_mapping = {
        1: 4,
        2: 4,
        3: 4,
        4: 4,
        5: 4,
        6: 4,
        7: 3,
        8: 3,
        9: 3,
    }
    
    # if any of sections 7, 8, or 9 have value, map changes to 7:2, 8:2, 9:3
    has_value = False
    for i in range(6,9):
      row_index = (i) // 3
      col_index = (i) % 3
      row_start = row_index * section_height
      row_end = row_start + section_height
      col_start = col_index * section_width
      col_end = col_start + section_width
      section = input_grid[row_start:row_end, col_start:col_end]
      if np.any(section):
          has_value = True
          break
    if has_value:
       output_mapping[7] = 2

    # if any of sections 1, 2, or 3 have value, map changes to 1:3, 2:4, 3:4
    has_value = False
    for i in range(0,3):
      row_index = (i) // 3
      col_index = (i) % 3
      row_start = row_index * section_height
      row_end = row_start + section_height
      col_start = col_index * section_width
      col_end = col_start + section_width
      section = input_grid[row_start:row_end, col_start:col_end]
      if np.any(section):
          has_value = True
          break
    if has_value:
       output_mapping[1] = 3
    

    # Process each section
    for i in range(9):
        row_index = (i) // 3
        col_index = (i) % 3
        row_start = row_index * section_height
        row_end = row_start + section_height
        col_start = col_index * section_width
        col_end = col_start + section_width

        section = input_grid[row_start:row_end, col_start:col_end]
        
        output_grid[row_index,col_index] = output_mapping.get(i+1, 0)


    return output_grid.tolist()