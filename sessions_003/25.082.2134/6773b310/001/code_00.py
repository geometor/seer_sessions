"""
The input grid is divided into three horizontal sections based on the position of '8' (azure) pixels. 
A 3x3 output grid is generated. Each row of the output grid corresponds to a section of the input grid. 
If a '6' (magenta) pixel exists in a section *before* an 8, a '1' (blue) is placed in the output grid's corresponding row/column position. 
Otherwise, a '0' (white) is placed.
"""

import numpy as np

def get_sections(input_grid):
    """Divides the input grid into three sections based on the horizontal line of 8s."""
    rows, cols = input_grid.shape
    horizontal_line_row = -1
    for r in range(rows):
        if np.all(input_grid[r] == 8):
            horizontal_line_row = r
            break

    if horizontal_line_row == -1:  # Handle cases where the line isn't found (shouldn't happen based on prior)
        return [input_grid] #Return whole grid as one section
    
    top_section = input_grid[:horizontal_line_row]
    middle_section = input_grid[horizontal_line_row:horizontal_line_row+1] # The line itself
    bottom_section = input_grid[horizontal_line_row+1:]

    return top_section, middle_section, bottom_section
    

def check_for_magenta_before_azure(section):
    """Checks for the presence of '6' before '8' in each row of a section."""

    presence = [0, 0, 0]
    
    if section.size == 0:
        return presence
    
    rows, cols = section.shape
    for r in range(rows):
        for c in range(cols):
            if section[r,c] == 6:
               for c2 in range(c+1, cols):
                    if section[r,c2] == 8:
                        if c < (cols/3):
                            presence[0]=1
                        elif c < 2*(cols/3):
                            presence[1]=1
                        else:
                            presence[2] = 1
                        break # Found, go to the next row
            elif section[r, c] == 8:
                break # Found 8 first, move to next row
                
    return presence


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Divide the input grid into three sections
    top_section, middle_section, bottom_section = get_sections(input_grid)

    # Initialize the 3x3 output grid with all zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Check for magenta before azure in each section and generate output rows

    output_grid[0, :] = check_for_magenta_before_azure(top_section)
    output_grid[1, :] = check_for_magenta_before_azure(middle_section) #should always return 0
    output_grid[2, :] = check_for_magenta_before_azure(bottom_section)

    return output_grid