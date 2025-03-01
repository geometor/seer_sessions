# 77fdfe62 • 002 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by extracting non-blue, non-white, and non-azure colors from the top and bottom rows and arranging them in a new, smaller grid.
"""

import numpy as np

def extract_edge_colors(grid, row_indices):
    """Extracts colors from specified rows, excluding 1, 0, and 8."""
    colors = []
    for row_index in row_indices:
      row = grid[row_index]
      for col_index, color in enumerate(row):
          if color not in [1, 0, 8]:
              colors.append((col_index, color))
    return colors
def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Extract colors from top and bottom rows
    top_colors = extract_edge_colors(input_grid, [0])
    bottom_colors = extract_edge_colors(input_grid, [rows - 1])


    # Determine output grid size.  It seems output width == max col index of a target color
    max_col_top = max([c[0] for c in top_colors], default=-1)
    max_col_bottom = max([c[0] for c in bottom_colors], default=-1)

    output_width = max(max_col_top, max_col_bottom) + 1

    output_height = 0
    if len(top_colors) > 0:
        output_height += (len(top_colors) + output_width -1 ) // output_width
    if len(bottom_colors) > 0:
        output_height += (len(bottom_colors) + output_width - 1) // output_width

    output_height = max(output_height, 2) # ensure height is enough. Handles edge case in train_2.
    output_width = max(output_width, 2)  # at least a 2x2 output

    # Initialize output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Fill output grid with top colors
    row_index = 0
    col_offset = 0
    
    for col_index, color in top_colors:
        output_grid[row_index, col_index % output_width] = color
        if (col_index + 1) % output_width == 0:
            row_index +=1

    #Move to next available row
    row_index = (len(top_colors) + output_width - 1) // output_width


    # Fill output grid with bottom colors
    for col_index, color in bottom_colors:
        output_grid[row_index, col_index % output_width] = color
        if (col_index + 1) % output_width == 0:
            row_index += 1

    return output_grid.tolist()
```
