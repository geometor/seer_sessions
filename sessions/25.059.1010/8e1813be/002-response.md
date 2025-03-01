# 8e1813be • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Target Colors:** Examine the input grid and identify the colors that *completely fill one or more rows, and where the remaining pixels on that row are all 0*. Also the colors should be unique. For example, if color 2 appears twice as complete rows, ignore them.
2.  **Extract Rows:** For each target color identified, extract *one* full row of that color from the input grid. The width of the extracted row should be the same as the number of non-zero pixels in the original row.
3.  **Compose Output:** Stack the extracted rows vertically, in the order they appear top-to-bottom in the input, to create the output grid.
"""

import numpy as np

def get_unique_complete_rows(grid):
    """
    Identifies and returns unique complete rows of non-zero colors, along with their non-zero lengths
    """
    rows = []
    unique_colors = set()
    for row in grid:
        # Get unique non-zero elements
        non_zero_elements = np.unique(row[row != 0])

        #check non_zero_elements for uniqueness
        if len(non_zero_elements) == 1:
          color = non_zero_elements[0]
          if color not in unique_colors:
            unique_colors.add(color)
            non_zero_length = np.count_nonzero(row)
            rows.append( (row, non_zero_length) )    

    return rows

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Find complete rows and extract relevant portion
    rows_data = get_unique_complete_rows(input_grid)

    extracted_rows = []
    for row_data in rows_data:
        row, length = row_data
        extracted_rows.append(row[row != 0])

    # Compose output_grid
    if extracted_rows:
      output_grid = np.stack(extracted_rows)
    else:
      output_grid = np.array([])

    return output_grid.tolist()
```
