"""
1.  **Identify Gray Lines:** Find all vertical lines of gray (5) pixels.
2.  **Fill Above (Blue):** For each gray line, find the contiguous region of white (0) pixels *above* the top-most gray pixel in that line. Fill this region with blue (1) pixels. Stop if any non-white pixel is encountered.
3.  **Place Center Block (Red):** Find gray line segments that are two pixels and
    place a vertical 1x2 red (2) pixel block to the immediate right of those
    pixels.
4.  **Fill Below (Green):** For each gray line, find the contiguous regions of
    white (0) pixels immediately *below* any gray pixel that is not the bottom
    most row. Fill this region with green (3) pixels. Stop if any non-white pixel
    is encountered.
"""

import numpy as np

def find_gray_lines(grid):
    """Finds vertical lines of gray (5) pixels."""
    rows, cols = grid.shape
    gray_lines = []
    for c in range(cols):
        current_line = []
        for r in range(rows):
            if grid[r, c] == 5:
                current_line.append((r, c))
            elif current_line:
                gray_lines.append(current_line)
                current_line = []
        if current_line:  # Handle lines that extend to the bottom edge
            gray_lines.append(current_line)
    return gray_lines

def fill_above(grid, gray_lines):
    """Fills above gray lines with blue (1)."""
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    for line in gray_lines:
        top_r, top_c = line[0]
        for r in range(top_r - 1, -1, -1):
            if output_grid[r, top_c] == 0:
                output_grid[r, top_c] = 1
            else:
                break
    return output_grid

def place_center_block(grid, gray_lines):
    """Places 1x2 red block to the right of a 2-pixel gray segment"""
    rows, cols = grid.shape
    output_grid = np.copy(grid) # working on copy not original
    
    for line in gray_lines:
        if len(line) == 2:
           r1, c1 = line[0]
           if c1+1 < cols:
              output_grid[r1][c1+1] = 2
              output_grid[r1+1][c1+1] = 2
    
    return output_grid

def fill_below(grid, gray_lines):
    """Fills below gray lines with green (3), excluding bottom row."""
    rows, cols = grid.shape
    output_grid = np.copy(grid)
    for line in gray_lines:
        for r, c in line:
          if r+1 < rows:
            if output_grid[r+1][c] == 0:
                output_grid[r + 1, c] = 3

    return output_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify Gray Lines
    gray_lines = find_gray_lines(input_grid)

    # Fill Above (Blue)
    output_grid = fill_above(output_grid, gray_lines)

    # Place Center Block (Red)
    output_grid = place_center_block(output_grid, gray_lines)

    # Fill Below (Green)
    output_grid = fill_below(output_grid, gray_lines)

    return output_grid