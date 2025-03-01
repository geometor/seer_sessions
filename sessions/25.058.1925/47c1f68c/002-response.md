# 47c1f68c • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves identifying a cross-shaped object in the input grid, rotating it 90 degrees clockwise, potentially resizing it (reducing its thickness), and then placing it in the output grid. Isolated colored regions in the input are removed.
"""

import numpy as np

def find_cross(grid):
    """
    Identifies the cross-shaped object in the grid.
    Returns the color, center coordinates (row, col), and dimensions (horizontal, vertical) of the cross.
    Returns (None, None, None) if no cross is found.
    """
    rows, cols = grid.shape
    color_counts = {}
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                if color not in color_counts:
                    color_counts[color] = []
                color_counts[color].append((r, c))

    for color, cells in color_counts.items():
        # Check for horizontal and vertical lines
        rows_set = set(r for r, c in cells)
        cols_set = set(c for r, c in cells)

        if len(rows_set) > 1 and len(cols_set) > 1:
           
            horizontal_line = []
            vertical_line = []

            #check if there is an horizontal line
            for r in rows_set:
                continuous_cells = []
                current_group = []
                for c in range(0,cols):
                    if (r,c) in cells:
                        current_group.append((r,c))
                    else:
                        if len(current_group) > len(continuous_cells):
                            continuous_cells = current_group
                        current_group = []
                if len(current_group) > len(continuous_cells):
                            continuous_cells = current_group
                if len(continuous_cells)>1:
                    horizontal_line = continuous_cells

            #check if there is a vertical line
            for c in cols_set:
                continuous_cells = []
                current_group = []

                for r in range(0,rows):
                    if (r,c) in cells:
                        current_group.append((r,c))
                    else:
                        if len(current_group) > len(continuous_cells):
                            continuous_cells = current_group
                        current_group = []
                if len(current_group) > len(continuous_cells):
                            continuous_cells = current_group

                if len(continuous_cells)>1:
                    vertical_line = continuous_cells


            #check if there is intersection
            if len(horizontal_line) > 0 and len(vertical_line) >0:

                intersection = set(horizontal_line) & set(vertical_line)
                if len(intersection) > 0:
                    center_r = sum(r for r, c in cells) // len(cells)  #approximate center
                    center_c = sum(c for r, c in cells) // len(cells)


                    horizontal_length = len(horizontal_line)
                    vertical_length = len(vertical_line)
                    return color, (center_r, center_c), (horizontal_length, vertical_length)

    return None, None, None


def rotate_coordinates(r, c, center_r, center_c, rows, cols):
    """
    Rotates coordinates 90 degrees clockwise around a center point.
    Adjusts for the new grid size.
    """
    # Translate to origin
    r_translated = r - center_r
    c_translated = c - center_c

    # Rotate 90 degrees clockwise
    r_rotated = c_translated
    c_rotated = -r_translated

    # Translate back to center
    r_new = r_rotated + center_c #new center is the center of the original cross, new c is the center of rows
    c_new = c_rotated + center_r
    return int(r_new), int(c_new)

def reduce_thickness(cells):

    # Create a set for faster lookup
    cells_set = set(cells)
    
    # Remove cells to avoid non 1 thickness
    filtered_cells = []
    for r, c in cells:
        neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
        same_color_neighbors = 0
        for nr, nc in neighbors:
          if (nr,nc) in cells_set:
            same_color_neighbors +=1
        if same_color_neighbors < 3:
          filtered_cells.append((r,c))

    return filtered_cells



def transform(input_grid):
    """
    Transforms the input grid by rotating the cross-shaped object 90 degrees clockwise and placing it in the output grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)  # Initialize output_grid, rotated dimensions

    color, center, dimensions = find_cross(input_grid)

    if color is not None:
        cross_cells = []
        horizontal, vertical = dimensions
        center_r, center_c = center

        # Get cross cells with the original coordinates
        for r in range(rows):
            for c in range(cols):
                if input_grid[r,c] == color:
                    cross_cells.append((r,c))
       
        #reduce thickness
        cross_cells = reduce_thickness(cross_cells)
        # Rotate cells and place in output_grid
        for r, c in cross_cells:
           
            r_new, c_new = rotate_coordinates(r, c, center_r, center_c, rows, cols)

            if 0 <= r_new < cols and 0 <= c_new < rows:  # Check bounds for rotated grid
                output_grid[r_new, c_new] = color


    return output_grid
```
