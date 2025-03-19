# 5daaa586 • 020 • refine_coder

---
```python
"""
1.  **Row Selection:** Select rows from the input that contain a specific, non-zero color, and possibly 0's. Other colors should not be present. The specific color varies across examples (8, 3, 5, 6, and 7).
2.  **Zero Removal:** Remove all 0's from the selected rows.
3.  **Target Color Preservation:** Keep all instances of the target color.
4.  **Separator Insertion (Conditional):** If the target color is 8 or 6, insert a '4' between adjacent pixels of the target color *after* removing the zeros. Do not insert 4 if there are not adjacent pixels.
5. **Output:** The output grid consists of the modified selected rows. Each row becomes one row in the output.
"""

import numpy as np

def get_target_color(grid):
    """
    Identifies the target color for a given grid.
    The target color is a non-zero color that appears in the grid,
    and all non-zero cells must have this color. If multiple different
    non-zero colors are present, it returns None.
    """
    grid = np.array(grid)
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0]
    if len(non_zero_colors) == 1:
        return non_zero_colors[0]
    else:
        return None

def select_row(row, target_color):
    """
    Checks if a row should be selected based on the target color.
    A row is selected if it contains the target color and only 0s otherwise.
    """
    row = np.array(row)
    unique_colors = np.unique(row)
    for color in unique_colors:
      if color != 0 and color != target_color:
        return False
    return target_color in unique_colors
    

def process_row(row, target_color):
    """
    Processes a single row according to the rules: removes 0s,
    and inserts 4s if the target color is 8 or 6.
    """
    row = np.array(row)
    # Zero Removal
    row = row[row != 0]

    # Separator Insertion (Conditional)
    if target_color == 8 or target_color == 6:
        new_row = []
        for i in range(len(row)):
            new_row.append(row[i])
            if i < len(row) - 1:
                new_row.append(4)
        return new_row
    else:
        return list(row)  # Convert back to list


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    output_rows = []

    # Get Target color for row selection
    target_color = get_target_color(input_grid)

    if target_color is None:
      return np.array([])

    # Iterate over each row
    for row in input_grid:
        # Select Row
        if select_row(row, target_color):
            # Process the row
            processed_row = process_row(row, target_color)
            if len(processed_row) > 0:
              output_rows.append(processed_row)

    # Convert to a numpy array
    if len(output_rows) > 0:
      output_grid = np.array(output_rows)
    else:
      output_grid = np.array([])

    return output_grid
```
