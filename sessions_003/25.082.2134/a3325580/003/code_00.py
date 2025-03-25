"""
1.  **Identify Output Colors:**
    *   Iterate through each row of the input grid.
    *   For each row, store the set of non-zero colors present.
    *   Find colors that are present in the output grid.
2.  **Determine Output Height**: Find the number of the rows in the input up to the largest index of any color that is in the output.
3.  **Determine Output Order:**
    *   Examine the input rows.
    *   Find rows where all output colors are present. If multiple such rows exist, consider them to find the most consistent ordering of colors.
    *   Establish a consistent horizontal ordering of these colors from left to right based on these rows.
4.  **Construct Output Grid:**
    *   Create an output grid with the determined height.
    *   Each row of the output grid will contain the ordered sequence of output colors.
"""

import numpy as np

def get_row_colors(input_grid):
    """Gets the set of non-zero colors present in each row."""
    row_colors = []
    for row in input_grid:
        colors = sorted(list(set(row[row != 0])))
        row_colors.append(colors)
    return row_colors

def get_output_colors(output_grid):
    """Gets the set of colors present in the output grid."""
    return sorted(list(set(output_grid.flatten())))
    
def get_common_colors(input_grid, output_grid):
  """Find common colors in input and output grid"""
  input_colors = set(input_grid.flatten())
  output_colors = set(output_grid.flatten())

  return sorted(list(input_colors.intersection(output_colors)))
  
def determine_output_height(input_grid, output_colors):
    """Determines the height of the output grid."""
    
    max_index = 0
    for color in output_colors:
        for i, row in enumerate(input_grid):
            if color in row:
              max_index = max(i, max_index)
    return max_index + 1

def determine_output_order(input_grid, output_colors, row_colors):
    """Determines the horizontal order of colors in the output."""
    # Find rows containing all output colors
    candidate_rows = []
    for i, colors in enumerate(row_colors):
        if all(color in colors for color in output_colors):
            candidate_rows.append(i)

    # Determine order based on candidate rows
    if candidate_rows:
        # Use the first candidate row to determine order
        first_row_index = candidate_rows[0]
        ordered_colors = []
        for cell in input_grid[first_row_index]:
          if cell in output_colors and cell not in ordered_colors:
            ordered_colors.append(cell)
        return ordered_colors

    # Fallback: use existing output colors
    return output_colors


def transform(input_grid, output_grid): # Added output_grid as parameter
    # Identify output colors
    # row_colors = get_row_colors(input_grid)
    # output_colors = get_output_colors(output_grid) # Use provided output

    common_colors = get_common_colors(input_grid, output_grid)

    row_colors = get_row_colors(input_grid)
    # Determine output height
    output_height = determine_output_height(input_grid, common_colors)

    # Determine output order
    output_order = determine_output_order(input_grid, common_colors, row_colors)
    #remove 0 from output order:
    output_order = [c for c in output_order if c!= 0]
    
    # Construct output grid
    output_grid_result = np.zeros((output_height, len(output_order)), dtype=int)
    for i in range(output_height):
        output_grid_result[i, :] = output_order

    return output_grid_result