# 5bd6f4ac • 002 • example_4 • investigate_coder

---
```python
"""
The transformation extracts the top-right 3x3 subgrid of non-zero elements from the input grid, where all zero rows are kept, but not all zero columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid according to the rule.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    output_array = np.zeros((3, 3), dtype=int)

    # Find the rightmost column index with a non-zero element.
    rightmost_col = -1
    
    selected_rows = []
    for r in range(rows):
        row = input_array[r]
        last_non_zero_col = -1
        
        for c in range(cols -1, -1, -1):
            if row[c] != 0:
                last_non_zero_col = c
                break;

        selected_rows.append(last_non_zero_col)

    #fill output grid
    out_row = 0
    for in_row in range(rows):        
        if selected_rows[in_row] != -1 or (rows -1 - in_row) < 3 :
            if out_row < 3 :
              start_col = selected_rows[in_row] - 2 if selected_rows[in_row] -2 >= 0 else 0
              if selected_rows[in_row] != -1 :
                
                for out_col in range(3):
                  in_col = start_col + out_col                  
                  if in_col <= selected_rows[in_row] and in_col >= 0:
                    output_array[out_row,out_col] = input_array[in_row,in_col]
                  else:
                    output_array[out_row,out_col] = 0
              else:
                  output_array[out_row,:] = [0,0,0]
              out_row += 1

    return output_array.tolist()
```
