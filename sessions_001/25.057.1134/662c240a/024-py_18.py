"""
The input grid is vertically divided into three equal sections. The output grid corresponds to the section of the input grid that contains a unique color that doesn't appear in the other two sections.
"""

import numpy as np

def find_unique_color_section(input_grid):
    """
    Divides the input grid into three vertical sections and identifies the section
    with a unique color.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    subgrid_height = height // 3

    sections_colors = []
    for i in range(3):
        start_row = i * subgrid_height
        end_row = start_row + subgrid_height
        subgrid = input_grid[start_row:end_row, :]
        sections_colors.append(set(np.unique(subgrid)))

    # Find unique colors in each section
    unique_colors = []
    for i in range(3):
      other_sections_colors = set()
      for j in range(3):
        if i != j:
          other_sections_colors = other_sections_colors.union(sections_colors[j])
      unique_colors.append(sections_colors[i] - other_sections_colors)

    # identify the section with unique color(s)
    for i, unique_color_set in enumerate(unique_colors):
        if len(unique_color_set) > 0:
            return i + 1 #section are 1 based
    
    return None # No unique section. Should not happen in training data.

def transform(input_grid):
    """
    Transforms the input grid by selecting the section with a uniquely colored region.
    """
    # Find the section with unique colors.
    section_number = find_unique_color_section(input_grid)
    input_grid = np.array(input_grid)
    height = input_grid.shape[0]
    subgrid_height = height // 3

    # Select the subgrid by section.
    if section_number is not None:
      start_row = (section_number - 1) * subgrid_height
      output_grid = input_grid[start_row:start_row + subgrid_height, :]
    else: # use first section as default
      output_grid = input_grid[0:subgrid_height, :]

    return output_grid.tolist()