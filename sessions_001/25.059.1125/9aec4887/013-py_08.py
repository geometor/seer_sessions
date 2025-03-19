"""
1.  **Identify the Input Line:** Find the contiguous vertical line of non-zero pixels in the input grid. If there are no such pixels return an empty 5x5 output. Note the color of the line. Note the length of the vertical line.
2.  **Determine output size and separation:** The output grid is always 5x5. If the length of the input line is 1, the white space separating the output is three rows, making the colored pixels separated by a total of 4 rows and 2 columns. If the length of the input line is greater than one, then the white space separating the mirrored lines is 1 column.
3. **Scale the Line:** Scale the input line so that the mirrored lines in the ouput will fit completely within the ouput grid.
4.  **Mirror and Create Output:** Create a 5x5 output grid. Place a copy of the (scaled) input line in the output grid, centered vertically. Then using the rule about separation, create its mirror image.
"""

import numpy as np

def get_vertical_line(grid):
    """
    Finds the longest contiguous vertical line of non-zero pixels.
    Returns a tuple: (color, [(row, col), ...]) or (None, []) if no line is found.
    """
    max_len = 0
    longest_line = []
    line_color = None

    for col in range(grid.shape[1]):
        for start_row in range(grid.shape[0]):
            color = grid[start_row, col]
            if color != 0:
                current_line = []
                row = start_row
                while row < grid.shape[0] and grid[row, col] == color:
                    current_line.append((row, col))
                    row += 1

                if len(current_line) > max_len:
                    max_len = len(current_line)
                    longest_line = current_line
                    line_color = color

    return line_color, longest_line

def scale_line(line, max_length):
    """Scales a line to fit within a given maximum length."""
    if len(line) <= max_length:
        return line
    
    # scale down to fit in the 5x5 output grid.
    scale_factor = (max_length) / len(line)    
    new_length = int(len(line) * scale_factor)
    
    # select equally spaced pixels
    indices = np.linspace(0, len(line) - 1, new_length, dtype=int)
    scaled_line = [line[i] for i in indices]
    
    return scaled_line
    

def transform(input_grid):
    """Transforms the input grid according to the mirroring rule."""

    # initialize output grid
    output_grid = np.zeros((5, 5), dtype=int)
    
    # find input line 
    color, line = get_vertical_line(input_grid)

    # handle no line found
    if not line:
        return output_grid

    # determine separation and output placement
    if len(line) == 1:
        separation = 3
        line = scale_line(line, 1) # single pixel line
        row_start = 0 # top of output
        col_1 = 1
        col_2 = 3
        for r, c in line:
            output_grid[row_start, col_1] = color
            output_grid[row_start + 4, col_1] = color # other row

            output_grid[row_start, col_2] = color
            output_grid[row_start + 4, col_2] = color # other row
    else:
        separation = 1
        
        scaled_line = scale_line(line, 4) # fit the output grid
            
        # center line in 5x5
        row_start = (5 - len(scaled_line)) // 2

        
        col_1 = 1
        col_2 = 3
        
        for i, (r, c) in enumerate(scaled_line):
            if row_start + i < 5:  # stay within 5x5 grid
                output_grid[row_start + i, col_1] = color
                output_grid[row_start + i, col_2] = color

    return output_grid