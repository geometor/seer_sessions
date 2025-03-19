# bc1d5164 • 032 • refine_coder

---
```python
"""
1.  **Identify Dominant Non-Zero Colors:** For each row and each column, determine the most frequent non-zero color. If a row or column contains *only* zero (white), it is skipped.
2.  **Create Intersection Sets:** Create a set of "target rows" and a set of "target columns." A row is a "target row" if its most frequent non-zero color appears in *any* of the "target columns" as a dominant color. Vice-versa for columns.
3.  **Extract Subgrid:** Create a new grid (the output grid) composed of the cells that are at the intersection of the target rows and target columns. The values of these cells should remain the same as in the original input.
4. If there are no zero (white) pixels, there is no transformation.
"""

import numpy as np
from collections import Counter

def get_dominant_nonzero_color(arr):
    """Finds the most frequent non-zero color in a 1D array."""
    counts = Counter(arr)
    # Remove zero (white) from consideration
    if 0 in counts:
        del counts[0]
    if not counts:
        return 0  # Return 0 if no non-zero colors are present
    return counts.most_common(1)[0][0]

def transform(input_grid):
    """Extracts the subgrid based on dominant non-zero colors in rows and columns."""
    
    input_grid = np.array(input_grid)
    
    # Check if the grid contains any zero (white) pixels
    if 0 not in input_grid:
        return input_grid.tolist()  # No transformation needed

    rows, cols = input_grid.shape
    
    # Identify dominant non-zero colors for each row
    row_dominant_colors = [get_dominant_nonzero_color(input_grid[i,:]) for i in range(rows)]
    
    # Identify dominant non-zero colors for each column
    col_dominant_colors = [get_dominant_nonzero_color(input_grid[:,j]) for j in range(cols)]

    # Create target row and column sets
    target_rows = set()
    target_cols = set()

    for i in range(rows):
        if row_dominant_colors[i] != 0:  # Skip rows with only zeros
             for j in range(cols):
                if col_dominant_colors[j] !=0 and row_dominant_colors[i] == col_dominant_colors[j]:
                    target_rows.add(i)
                    target_cols.add(j)
                
    # Handle cases where rows or columns are all zeros
    if not target_rows:
        for i, color in enumerate(row_dominant_colors):
            if color != 0: target_rows.add(i)

    if not target_cols:
      for j, color in enumerate(col_dominant_colors):
            if color != 0: target_cols.add(j)
    # Extract subgrid, handling empty target_rows or target_cols
    if target_rows and target_cols:
      output_grid = input_grid[np.ix_(list(target_rows), list(target_cols))]
      return output_grid.tolist()
    else:
      return []
```
