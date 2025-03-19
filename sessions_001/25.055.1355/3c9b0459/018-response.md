# 3c9b0459 • 018 • refine_coder

---
```python
"""
The transformation rule converts horizontal lines of pixels into vertical lines of the same color and length. The column of the vertical line is determined by the starting column and length of the horizontal line.
Special case: full rows become full rectangles.
"""

import numpy as np

def get_horizontal_lines(grid):
    """
    Identifies contiguous horizontal lines in the grid.
    Returns a list of lines, each represented as a dictionary.
    """
    lines = []
    for row_idx, row in enumerate(grid):
        current_line = []
        for col_idx, pixel in enumerate(row):
            if not current_line:
                current_line.append((col_idx, pixel))
            elif pixel == current_line[-1][1]:
                current_line.append((col_idx, pixel))
            else:
                if len(current_line) > 0:
                    lines.append({
                        'row': row_idx,
                        'start_col': current_line[0][0],
                        'end_col': current_line[-1][0],
                        'color': current_line[0][1],
                        'length': len(current_line)
                    })
                current_line = [(col_idx, pixel)]
        if len(current_line) > 0:
            lines.append({
                'row': row_idx,
                'start_col': current_line[0][0],
                'end_col': current_line[-1][0],
                'color': current_line[0][1],
                'length': len(current_line)
            })
    return lines

def transform(input_grid):
    """
    Transforms horizontal lines to vertical lines based on the rule.
    """
    input_np = np.array(input_grid)
    output_grid = np.zeros_like(input_np)

    # Check for full rows (special case)
    full_rows = []
    for i,row in enumerate(input_np):
        if np.all(row != 0) and len(np.unique(row)) == 1:
            full_rows.append(i)
    
    if full_rows:
        color = input_np[full_rows[0]][0]
        height = len(full_rows)
        width = len(input_np[0])
        new_array = np.full((width, height),color)
        output_grid = new_array.T.tolist()
        return output_grid # return early since this is the special case

    # Get horizontal lines
    lines = get_horizontal_lines(input_grid)

    # Transform each line
    for line in lines:
        length = line['length']
        color = line['color']
        start_row = line['row']
        start_col = line['start_col']

        new_col = start_col + (length // 2)
        new_row_start = start_row # - (length -1)  removed shift up
        
        # Create the vertical line
        for i in range(length):
            if new_row_start + i < len(output_grid) and new_col < len(output_grid[0]):
                output_grid[new_row_start + i][new_col] = color

    return output_grid.tolist()
```
