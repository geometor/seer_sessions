"""
Transforms the input grid by identifying and extracting uniform rows and columns.
Prioritizes full uniform rows. If uniform columns are present, it extracts those,
creating rows in the output grid where each cell represents a column's uniform color.
If there are no fully uniform rows, it looks for the longest uniform segment in
each row and constructs output rows using these segments.
"""

import numpy as np

def _find_uniform_rows(grid):
    """Identifies rows with a contiguous sequence of non-zero pixels of the same color."""
    uniform_rows = []
    for i, row in enumerate(grid):
        if _longest_uniform_subsequence(row) > 0:
             #check that the longest subsequence represents entire row by comparing it with count of non-zero
            color = -1
            count = 0
            for x in row:
                if x!= 0:
                    if color==-1:
                        color = x
                        count = 1
                    elif color == x:
                        count+=1

            if _longest_uniform_subsequence(row) == count:
                uniform_rows.append((i, row, 'full'))  # Store row index and the row itself, and flag "full"
            elif count>0:
                uniform_rows.append((i, row, 'partial'))
    return uniform_rows

def _longest_uniform_subsequence(row):
    """Finds the length of the longest uniform non-zero subsequence."""
    max_len = 0
    current_len = 0
    current_val = None
    for val in row:
        if val == current_val and val != 0:
            current_len += 1
        elif val != 0:
            max_len = max(max_len, current_len)
            current_len = 1
            current_val = val
        else:
            max_len = max(max_len, current_len)
            current_len = 0
            current_val = None

    max_len = max(max_len, current_len)  # Check at the end
    return max_len

def _find_uniform_columns(grid):
    """Finds columns with consistent non-zero values, allowing for 0s."""
    uniform_cols = []
    num_rows, num_cols = grid.shape
    for j in range(num_cols):
        first_val = None
        consistent = True
        for i in range(num_rows):
            if grid[i,j] != 0:
                if first_val is None:
                    first_val = grid[i, j]
                elif first_val != grid[i,j]:
                    consistent = False
                    break
        if first_val is not None and consistent:
            uniform_cols.append((j, first_val))
    return uniform_cols

def _extract_uniform_segment(row):
    """Extracts the longest uniform segment from a row."""
    max_len = 0
    current_len = 0
    current_val = None
    start_index = -1
    max_start_index = -1

    for i, val in enumerate(row):
        if val == current_val and val != 0:
            current_len += 1
        elif val != 0:
            if current_len > max_len:
                max_len = current_len
                max_start_index = start_index
            current_len = 1
            current_val = val
            start_index = i
        else:
            if current_len > max_len:
                max_len = current_len
                max_start_index = start_index
            current_len = 0
            current_val = None
            start_index = -1

    if current_len > max_len:
        max_len = current_len
        max_start_index = start_index

    if max_start_index != -1:
        return row[max_start_index : max_start_index + max_len]
    else:
        return np.array([])


def transform(input_grid):
    """Transforms the input grid based on uniform rows and columns."""

    uniform_rows = _find_uniform_rows(input_grid)
    uniform_columns = _find_uniform_columns(input_grid)
    # 1. Prioritize full uniform rows
    full_uniform_rows = [ (i,row) for i, row, flag in uniform_rows if flag == 'full']
    if full_uniform_rows:
        output_rows = [row for i, row in full_uniform_rows]
        output_grid = np.array(output_rows)
        if output_grid.size > 0:

          #now, reduce length
          first_output_row = output_grid[0,:]
          new_len = 0

          for x in first_output_row:
            if x!=0:
              new_len+=1

          output_grid_short = []
          for i in range(output_grid.shape[0]):
            output_grid_short.append(output_grid[i,:new_len])

          return np.array(output_grid_short)

    # 2. If uniform columns are present, use them
    if uniform_columns:
        output_rows = []
        for _, color in uniform_columns:
            output_rows.append([color] * len(uniform_columns)) # length = number of columns
        return np.array(output_rows)

    # 3.  Extract partial uniform rows
    partial_uniform_rows_with_segments = [ (i, _extract_uniform_segment(row))   for i, row, flag in uniform_rows if flag == 'partial']

    # 4. Sort by length
    sorted_partial = sorted(partial_uniform_rows_with_segments, key=lambda x: len(x[1]), reverse=True)
    if not sorted_partial:
        return np.array([]).reshape(0, 0)


    # 5. Construct the output based on max segment length
    max_seg_len = len(sorted_partial[0][1])

    output_grid = []
    for i, seg in sorted_partial:
      if len(seg)>0:
          output_grid.append(seg)

    if not output_grid:
      return np.array([]).reshape(0, 0)

    return np.array(output_grid)