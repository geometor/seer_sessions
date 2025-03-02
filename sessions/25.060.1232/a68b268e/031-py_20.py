"""
The input grid is divided by a horizontal blue line. The colors above and below this line are extracted and placed into a new grid. The output grid's first row is populated by colors found above the blue line, and its last row by colors found below the blue line. Intermediate rows are filled with black (0). The output grid size is determined by whether there are colors above or below the blue line.
"""

import numpy as np

def get_colors_relative_to_blue_line(grid):
    """
    Extracts non-blue (1) and non-white (0) colors above and below the horizontal blue line.
    """
    height, width = grid.shape
    blue_line_row = -1

    # Find the row index of the horizontal blue line
    for y in range(height):
        if all(grid[y, x] == 1 for x in range(width)):
            blue_line_row = y
            break

    colors = {
      'above_left': [],
      'above_right': [],
      'below_left': [],
      'below_right': []
    }
    
    if blue_line_row == -1:
        return colors

    # Extract colors above the blue line
    for y in range(blue_line_row):
        for x in range(width):
            if grid[y, x] != 1 and grid[y, x] != 0:
                if x < width // 2:
                    colors['above_left'].append(grid[y,x])
                else:
                    colors['above_right'].append(grid[y,x])
    
    # Extract colors below the blue line
    for y in range(blue_line_row + 1, height):
        for x in range(width):
            if grid[y, x] != 1 and grid[y,x] != 0:
                if x < width // 2:
                    colors['below_left'].append(grid[y,x])
                else:
                    colors['below_right'].append(grid[y,x])
    return colors

def transform(input_grid):
    # Convert input grid to numpy array
    grid = np.array(input_grid)

    # Extract colors relative to the blue line
    colors = get_colors_relative_to_blue_line(grid)

    # Determine output grid size and initialize
    above_exists = bool(colors['above_left'] or colors['above_right'])
    below_exists = bool(colors['below_left'] or colors['below_right'])
    
    num_rows = 0
    if above_exists:
        num_rows += 1
    if below_exists:
        num_rows += 1
    if above_exists and below_exists:
        num_rows = 4 # fixed size when both exist.

    output_grid = np.zeros((num_rows, 4), dtype=int)

    # Populate the first row if colors exist above the blue line
    if above_exists:
        output_grid[0, 0] = colors['above_left'][0] if colors['above_left'] else 0
        output_grid[0, 1] = colors['above_left'][-1] if len(colors['above_left']) > 1 else (colors['above_left'][0] if colors['above_left'] else 0)
        output_grid[0, 2] = colors['above_right'][0] if colors['above_right'] else 0
        output_grid[0, 3] = colors['above_right'][-1] if len(colors['above_right']) > 1 else (colors['above_right'][0] if colors['above_right'] else 0)

    # Populate the last row if colors exist below the blue line
    if below_exists:
        last_row = num_rows -1
        output_grid[last_row, 0] = colors['below_left'][0] if colors['below_left'] else 0
        output_grid[last_row, 1] = colors['below_left'][-1] if len(colors['below_left']) > 1 else (colors['below_left'][0] if colors['below_left'] else 0)
        output_grid[last_row, 2] = colors['below_right'][0] if colors['below_right'] else 0
        output_grid[last_row, 3] = colors['below_right'][-1] if len(colors['below_right']) > 1 else (colors['below_right'][0] if colors['below_right'] else 0)

    return output_grid.tolist()