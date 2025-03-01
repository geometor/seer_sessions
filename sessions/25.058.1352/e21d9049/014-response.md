# e21d9049 • 014 • refine_coder

---
```python
"""
The transformation rule involves identifying the smallest repeating unit (row, column, or block) in the input grid.
If a repeating row is found, the output is constructed by vertically tiling this row.
If a repeating column is found, the output is constructed by horizontally tiling this column.
If a repeating block is found, a more complex reflection/translation is checked.
"""

import numpy as np

def find_repeating_unit(input_grid):
    """Finds the smallest repeating unit (row, column, or block) in the grid."""
    rows, cols = input_grid.shape

    # Check for repeating rows
    for row_len in range(1, rows + 1):
        if rows % row_len == 0:
            unit = input_grid[:row_len, :]
            repeated = np.tile(unit, (rows // row_len, 1))
            if np.array_equal(repeated, input_grid):
                return unit, "row"

    # Check for repeating columns
    for col_len in range(1, cols + 1):
        if cols % col_len == 0:
            unit = input_grid[:, :col_len]
            repeated = np.tile(unit, (1, cols // col_len))
            if np.array_equal(repeated, input_grid):
                return unit, "col"

    # Check for repeating blocks (simplified for now - checks only square blocks.)
    for block_size in range(1, min(rows, cols) + 1):
      if rows % block_size == 0 and cols % block_size == 0:
        unit = input_grid[:block_size, :block_size]
        
        valid_block = True
        for row_start in range(0,rows,block_size):
            for col_start in range(0,cols,block_size):
                if not np.array_equal(unit, input_grid[row_start:row_start+block_size, col_start:col_start+block_size]):
                    valid_block = False
                    break
            if not valid_block:
                break
        if valid_block:
            return unit, "block"

    return None, None  # No repeating unit found


def determine_replication_rule(input_grid, unit, unit_type):
    """Determines how the repeating unit is replicated (reflection, translation)."""
    rows, cols = input_grid.shape
    unit_rows, unit_cols = unit.shape

    if unit_type == "row":
        return "translation", "vertical"
    elif unit_type == "col":
        return "translation", "horizontal"
    elif unit_type == 'block':
        # check for horizontal
        if np.array_equal(unit, np.fliplr(unit)):
           return "reflection", "horizontal"
        # check for vertical
        elif np.array_equal(unit, np.flipud(unit)):
           return "reflection", "vertical"

        return "translation", "both" # default
    
    return None, None



def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find the repeating unit.
    unit, unit_type = find_repeating_unit(input_grid)

    if unit is None:
        return output_grid  # No transformation if no repeating unit

     # Determine the replication rule.
    replication_type, direction = determine_replication_rule(input_grid, unit, unit_type)


    # Reconstruct the output.
    if replication_type == "translation":
        if direction == "vertical":
            output_grid = np.tile(unit, (rows // unit.shape[0], 1))
        elif direction == "horizontal":
            output_grid = np.tile(unit, (1, cols // unit.shape[1]))
        else: # both
           output_grid = np.tile(unit, (rows// unit.shape[0], cols // unit.shape[1]))
    elif replication_type == "reflection":
        if direction == "horizontal":
            output_grid = np.tile(unit, (rows// unit.shape[0],1))

            num_reps = cols // unit.shape[1]
            for i in range(num_reps):
                if (i+1)%2 == 0: # odd
                    output_grid[:,i*unit.shape[1]:(i+1)*unit.shape[1]] = np.fliplr(unit)

        elif direction == "vertical":
            output_grid = np.tile(unit, (1,cols // unit.shape[1]))

            num_reps = rows // unit.shape[0]
            for i in range(num_reps):
               if (i+1)%2 == 0: # odd
                    output_grid[i*unit.shape[0]:(i+1)*unit.shape[0],:] = np.flipud(unit)

    return output_grid
```
