"""
The input grid is transformed into a 3x9 output grid. The output grid is divided into three 3x3 sections. 
Each section of the output grid is filled with a color. 
The color is determined by inspecting the corresponding section of the input grid.
The input grid is divided into three equal-width sections.
For each section, a color is assigned based on the presence and position of gray (5) pixels:
- If gray (5) is present in the section, a specific color based on index is assigned.
- If gray (5) is not present, another default color is assigned.
"""

import numpy as np

def get_section_color(input_section):
    """
    Determines the output color for a section based on the presence of gray (5).
    """
    rows, cols = input_section.shape
    
    for c in range(cols):
      for r in range(rows):
        if input_section[r,c] == 5:
          if c < cols //3 :
             return 6
          elif c< (2*cols) // 3:
             return 3
          else: 
             return 9 if cols>2 else 4
    return 1 if cols >2 else 4

def transform(input_grid):
    """
    Transforms the input grid into a 3x9 output grid based on the described rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Initialize the output grid
    output_grid = np.zeros((3, 9), dtype=int)

    # Divide the input grid into three sections
    section_width = cols // 3
    sections = []
    
    if section_width == 0: # Handle cases where cols < 3, must pad sections with zeros
        sections = [np.array([[0, 0, 0]])] *3

    
    elif section_width*3 != cols:
      sections = [input_grid[:, 0 : section_width], input_grid[:, section_width: 2* section_width],input_grid[:, 2*section_width:]]
      if sections[2].shape[1]>section_width:
          padded_section = np.pad(sections[2], ((0,0),(0, 3-sections[2].shape[1])), 'constant')
          sections[2] = padded_section

    else:
      sections = [input_grid[:, i * section_width:(i + 1) * section_width] for i in range(3)]


    # Determine the color for each section
    colors = [get_section_color(section) for section in sections]

    # Fill the output grid
    for i in range(3):
        output_grid[:, i * 3:(i + 1) * 3] = colors[i]

    return output_grid.tolist()