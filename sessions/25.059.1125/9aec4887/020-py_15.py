"""
1. **Identify Colored Lines:** In each input grid, identify horizontal lines of colors orange (7), blue (1), yellow (4), and magenta (6).
2. **Identify Colored Shapes**: In each input grid, identify the azure(8) shape, and any other shapes of different colors that appear inside the space between the colored lines.
3. **Determine Subgrid:** A region of interest exists between the horizontal lines.
4. **Extract:** Extract the subgrid that encloses all pixels of the azure shape and any enclosed shapes, including the colored horizontal lines.
5.  **Reduce**: Create output, collapsing the extracted subgrid by removing 0 value columns from sides.
"""

import numpy as np

def find_horizontal_lines(grid, colors):
    """Finds horizontal lines of specified colors."""
    lines = {}
    for color in colors:
        rows = np.where(np.all(grid == color, axis=1))[0]
        if rows.size > 0:
            lines[color] = rows
    return lines

def find_other_shapes(grid, line_colors):
    """Finds shapes of colors not in line_colors within the region of interest."""

    other_colors = [c for c in np.unique(grid) if c not in line_colors and c != 0] #Remove background color
    shapes = {}
    for color in other_colors:
        shapes[color] = np.argwhere(grid == color)
    return shapes
    

def extract_subgrid(grid, lines, shapes):
    """Extracts the subgrid enclosing lines and shapes."""

    min_row = min(lines.values(), key=min)
    if isinstance(min_row, np.ndarray):
      min_row = min_row[0]

    max_row = max(lines.values(), key=max)
    if isinstance(max_row, np.ndarray):
        max_row = max_row[0]
    
    all_coords = []

    for shape_coords in shapes.values():
        if len(shape_coords) > 0:  # Check if the array is not empty
          all_coords.extend(shape_coords)

    if len(all_coords) == 0: #If no shapes between lines, min and max should come from lines
      min_col = 0
      max_col = grid.shape[1]-1
    else:
      all_coords = np.array(all_coords)
      min_col = np.min(all_coords[:, 1])
      max_col = np.max(all_coords[:, 1])

    #Extract the horizontal lines as well
    min_col = min(min_col, 0)
    max_col = max(max_col, grid.shape[1]-1)

    return grid[min_row:max_row+1, min_col:max_col+1]


def transform(input_grid):
    # Identify colored lines
    line_colors = [7, 1, 4, 6]
    lines = find_horizontal_lines(input_grid, line_colors)

    # Identify other shapes
    shapes = find_other_shapes(input_grid, line_colors)

    # Extract the subgrid
    subgrid = extract_subgrid(input_grid, lines, shapes)

    # Remove 0 columns
    non_zero_cols = np.any(subgrid != 0, axis=0)
    output_grid = subgrid[:, non_zero_cols]

    return output_grid