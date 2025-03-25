```python
"""
Extracts a sub-grid from the input grid. The sub-grid is located above a horizontal marker line of uniform color.
The height of the sub-grid is determined by the row index of the marker line. The width is determined by
the location of first occurrence of the second color before the marker row.
"""

import numpy as np

def find_marker_line(grid):
    """Finds the topmost horizontal line with all pixels of the same color."""
    for i, row in enumerate(grid):
        if np.all(row == row[0]):
            return i
    return -1  # No marker line found

def find_first_occurence_column(grid, marker_row):
    """Finds the column index of first occurence of the second color from top."""
    
    if (marker_row == -1):
        return len(grid[0]) if len(grid) > 0 else 0
    
    if (marker_row == 0):
        return len(grid[0]) if len(grid) > 0 else 0
    
    rows_to_scan = grid[:marker_row]
    first_color = -1
    second_color = -1
    
    for i in range(len(rows_to_scan)):
        for j in range(len(rows_to_scan[0])):
            if first_color == -1 :
                first_color = rows_to_scan[i][j]
            else:
                if (rows_to_scan[i][j] != first_color):
                    if(second_color == -1 or rows_to_scan[i][j] < second_color):
                        second_color = rows_to_scan[i][j]
                        
    
    if (second_color == -1):
        return len(rows_to_scan[0]) if len(rows_to_scan) > 0 else 0
    
    
    for i in range(len(rows_to_scan)):
        for j in range(len(rows_to_scan[0])):
            if rows_to_scan[i][j] == second_color:
                return j
    
    return len(grid[0]) if len(grid) > 0 else 0

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Find the marker line
    marker_row = find_marker_line(input_grid)

    # Determine output height
    output_height = marker_row if marker_row != -1 else input_grid.shape[0]

    # Determine the output width.
    output_width = find_first_occurence_column(input_grid, marker_row) + 1

    # Extract the sub-grid
    output_grid = input_grid[:output_height, :output_width]

    return output_grid.tolist()
```