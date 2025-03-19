"""
1.  **Identify the longest vertical line:** Find the longest vertical line of non-zero pixels in the input grid.  Note the color and position of this line.
2.  **Identify the longest horizontal line of same color:** find the longest horizontal line of the same color, but exclude any horizontal lines that do not contain pixels adjacent to the veritical line.
3.  **Copy Vertical Line:** Copy the pixels of the longest vertical line to the output grid, maintaining their original vertical positions and centering horizontally.
4.  **Copy Horizontal Line (Second-to-last Row):** Copy the longest qualified horizontal line to the second-to-last row of the output grid.
5. **Empty Grid Condition:** If no vertical line, or no qualified horizontal line is found, return an empty grid of the same dimensions as the input.
"""

import numpy as np

def find_longest_vertical_line(grid):
    rows, cols = grid.shape
    longest_line = []
    line_color = 0
    center_col = -1

    for c in range(cols):
        current_line = []
        for r in range(rows):
            if grid[r, c] != 0:
                current_line.append((r, c))
        if len(current_line) > len(longest_line):
            longest_line = current_line
            if len(longest_line) > 0:
                line_color = grid[longest_line[0][0], longest_line[0][1]]
                center_col = c

    return longest_line, line_color, center_col

def find_longest_horizontal_line(grid, vertical_line_color, vertical_line_col):
    rows, cols = grid.shape
    longest_line = []
    
    if vertical_line_col == -1:
        return longest_line

    for r in range(rows):
        current_line = []
        for c in range(cols):
            if grid[r, c] == vertical_line_color:
                current_line.append((r,c))
        
        valid_line = False
        for r1,c1 in current_line:
            if abs(c1-vertical_line_col) <= 1 and grid[r1,vertical_line_col] == vertical_line_color:
                valid_line = True
                break
        
        if valid_line and len(current_line) > len(longest_line):
            longest_line = current_line

    return longest_line

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Find the longest vertical line
    vertical_line, vertical_line_color, center_col = find_longest_vertical_line(input_grid)

    # Find the longest horizontal line of the same color and adjacent
    horizontal_line = find_longest_horizontal_line(input_grid, vertical_line_color, center_col)
    
    # If no vertical line or no qualified horizontal line, return empty grid
    if not vertical_line or not horizontal_line:
        return output_grid

    # Copy vertical line
    for r, c in vertical_line:
        output_grid[r, center_col] = vertical_line_color

    # Copy horizontal line to the second-to-last row
    for r, c in horizontal_line:
        output_grid[rows - 2, c] = vertical_line_color
        
    return output_grid