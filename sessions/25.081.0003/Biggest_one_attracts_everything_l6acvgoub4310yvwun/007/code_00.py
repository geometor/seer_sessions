"""
The transformation rule works as follows:
1. Identify Non-Empty Rows: Examine each row in the input grid. A row is "non-empty" if it contains any digit other than 0.

2. Shift Non-Empty Rows Upwards: Arrange all non-empty rows sequentially at the top of the output grid, maintaining their original relative order.

3. Rearrange Non-Zero Digits Within Rows: Within each non-empty row, rearrange the non-zero digits based on these principles:
    *   Zeroes to the left of non-zero digits: remain to the left.
    *   Zeroes to the right: pad the remaining space.
    *   Merging: If two rows have non-zero values and all values are equal except
        the last, then consolidate to a single row.

4. Fill Remaining Rows: Insert empty (all 0) rows to the bottom of the grid until the input and output grid have the same height.
"""

import numpy as np

def is_empty_row(row):
    """Checks if a row is empty (all zeros)."""
    return all(pixel == 0 for pixel in row)

def rearrange_row(row):
    """Rearranges non-zero digits within a row, keeping leading zeros."""
    non_zero_digits = [pixel for pixel in row if pixel != 0]
    num_leading_zeros = 0
    for pixel in row:
        if pixel == 0:
            num_leading_zeros += 1
        else:
            break
    new_row = [0] * num_leading_zeros + non_zero_digits
    
    while len(new_row) < len(row):
      new_row.append(0)
    return new_row
    

def merge_rows(rows):
    """Merges rows that are identical except for the last non-zero digit."""
    merged_rows = []
    skip_indices = set()

    for i in range(len(rows)):
        if i in skip_indices:
            continue

        current_row = rows[i]
        merged = False

        for j in range(i + 1, len(rows)):
            if j in skip_indices:
              continue
            
            next_row = rows[j]

            non_zero_current = [x for x in current_row if x!=0]
            non_zero_next = [x for x in next_row if x != 0]

            if len(non_zero_current) > 0 and len(non_zero_next) > 0:
              if len(non_zero_current) == len(non_zero_next):
                if non_zero_current[:-1] == non_zero_next[:-1]:
                    # Merge: keep the row with larger last digit
                    
                    merged_row = current_row[:] #copy
                    
                    idx_cur = len(current_row) - current_row[::-1].index(non_zero_current[-1])-1
                    idx_next = len(next_row) - next_row[::-1].index(non_zero_next[-1])-1
                   
                    if idx_cur != idx_next and non_zero_current[-1] != non_zero_next[-1]:
                      # can merge if last non_zero is in same index
                      continue

                    if non_zero_current[-1] > non_zero_next[-1]:
                      merged_row[idx_cur] = non_zero_current[-1]
                      merged_rows.append(rearrange_row(merged_row))
                      skip_indices.add(j)
                      merged = True
                      break # only merge once
                    else:
                      merged_row[idx_next] = non_zero_next[-1]
                      merged_rows.append(rearrange_row(merged_row))
                      skip_indices.add(j)
                      merged=True
                      break
        if not merged:
            merged_rows.append(rearrange_row(current_row))


    return merged_rows

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    output_grid = []

    # Identify and shift non-empty rows
    non_empty_rows = []
    for row in input_grid_np:
        if not is_empty_row(row):
            non_empty_rows.append(list(row))

    # Merge and rearrange within non-empty rows
    merged_rows = merge_rows(non_empty_rows)

    # Add non-empty rows to output
    for row in merged_rows:
        output_grid.append(row)

    # Pad with empty rows at top and bottom
    num_empty_rows = rows - len(output_grid)
    
    while len(output_grid) < rows :
       output_grid.append([0] * cols)

    return output_grid