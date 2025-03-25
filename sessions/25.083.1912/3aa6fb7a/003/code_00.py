"""
The transformation rule identifies horizontal or vertical lines of azure (8) pixels. 
It then inserts blue (1) pixels between these lines to connect them. The blue 
pixels fill the space between the azure lines, but only along rows or columns, 
never diagonally. The blue pixels are inserted in the cells immediately adjacent 
to the azure pixels, effectively forming a continuous line or block of azure 
and blue pixels.
"""

import numpy as np

def find_azure_lines(grid):
    """
    Identifies horizontal and vertical lines of azure (8) pixels.
    Returns a list of lines, where each line is a list of (row, col) coordinates.
    """
    azure_lines = []
    rows, cols = grid.shape

    # Check for horizontal lines
    for r in range(rows):
        line = []
        for c in range(cols):
            if grid[r, c] == 8:
                line.append((r, c))
            elif line:
                if len(line) > 0:  # Changed from > 1
                    azure_lines.append(line)
                line = []
        if line:
            if len(line) > 0: # Changed from >1
                azure_lines.append(line)

    # Check for vertical lines
    for c in range(cols):
        line = []
        for r in range(rows):
            if grid[r, c] == 8:
                line.append((r, c))
            elif line:
                if len(line) > 0: # Changed from > 1
                    azure_lines.append(line)
                line = []
        if line:
            if len(line) > 0: # Changed from >1
                azure_lines.append(line)

    return azure_lines

def transform(input_grid):
    """
    Transforms the input grid by inserting blue pixels between azure lines.
    """
    output_grid = np.copy(input_grid)
    azure_lines = find_azure_lines(output_grid)

    # Iterate through pairs of lines to find potential insertion points
    for i in range(len(azure_lines)):
        for j in range(i + 1, len(azure_lines)):
            line1 = azure_lines[i]
            line2 = azure_lines[j]

            # Check if lines are parallel and on the same row or column
            if all(r1 == line1[0][0] for r1, _ in line1) and all(r2 == line2[0][0] for r2, _ in line2):  # Horizontal lines
                r = line1[0][0]
                if abs(line2[0][0] - r) == 0: # same row
                    cols1 = sorted([c for _, c in line1])
                    cols2 = sorted([c for _, c in line2])
                    # Find insertion points between lines
                    for c in range(min(cols1[-1], cols2[-1]), max(cols1[0],cols2[0])):
                        if output_grid[r,c] == 0:
                            output_grid[r,c] = 1

            elif all(c1 == line1[0][1] for _, c1 in line1) and all(c2 == line2[0][1] for _, c2 in line2):  # Vertical lines

                c = line1[0][1]
                if abs(line2[0][1] - c) == 0: # same col
                    rows1 = sorted([r for r, _ in line1])
                    rows2 = sorted([r for r, _ in line2])
                    # Find insertion points between lines.
                    for r in range(min(rows1[-1], rows2[-1]), max(rows1[0], rows2[0])):
                        if output_grid[r,c] == 0:
                            output_grid[r,c] = 1
            # New logic for connecting adjacent horizontal/vert
            else:
              # Check if lines are adjacent horizontally
              if all(r1 == line1[0][0] for r1, _ in line1) and all(r2 == line2[0][0] for r2, _ in line2) :
                  if abs(line1[0][0] - line2[0][0]) == 1:  # Check if rows are adjacent

                      c1_min = min(c for _,c in line1)
                      c1_max = max(c for _,c in line1)
                      c2_min = min(c for _,c in line2)
                      c2_max = max(c for _,c in line2)

                      c_min = max(c1_min,c2_min)
                      c_max = min(c1_max,c2_max)
                      if line2[0][0] > line1[0][0]:
                        r = line2[0][0]
                      else:
                        r = line1[0][0]
                      for c in range(c_min, c_max+1):
                          if output_grid[r-1,c] == 0:
                              output_grid[r-1,c] = 1

              # Check if lines are adjacent vertically
              if all(c1 == line1[0][1] for _, c1 in line1) and all(c2 == line2[0][1] for _, c2 in line2) :
                  if abs(line1[0][1] - line2[0][1]) == 1: # Check if columns are adjacent

                    r1_min = min(r for r,_ in line1)
                    r1_max = max(r for r,_ in line1)
                    r2_min = min(r for r,_ in line2)
                    r2_max = max(r for r,_ in line2)

                    r_min = max(r1_min,r2_min)
                    r_max = min(r1_max,r2_max)

                    if line2[0][1] > line1[0][1]:
                        c = line2[0][1]
                    else:
                        c = line1[0][1]

                    for r in range(r_min,r_max + 1):
                        if output_grid[r, c-1] == 0:
                          output_grid[r,c-1] = 1

    return output_grid