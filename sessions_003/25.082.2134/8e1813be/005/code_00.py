"""
Transforms the input grid based on consistent columns or uniform rows.

Prioritizes extracting full-height uniform columns. If none are found,
selects rows with uniform non-zero color segments, filters them by maximum
length, and orders them by a predefined color priority.
"""

import numpy as np

def _find_consistent_columns(grid):
    """Finds columns with consistent non-zero values spanning the full height."""
    consistent_cols = []
    num_rows, num_cols = grid.shape
    for j in range(num_cols):
        first_val = grid[0, j]
        if first_val != 0 and np.all(grid[:, j] == first_val):
            consistent_cols.append(j)
    return consistent_cols

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
                uniform_rows.append((i, row))  # Store row index and the row itself
    return uniform_rows


def transform(input_grid):
    """Transforms the input grid based on consistent columns or uniform rows."""

    # 1. Check for Uniform Columns
    consistent_columns = _find_consistent_columns(input_grid)
    if consistent_columns:
        # Extract these columns, preserving their original order.
        output_grid = input_grid[:, consistent_columns]
        return output_grid

    # 2. If no uniform columns: select rows with uniform segments.
    uniform_rows = _find_uniform_rows(input_grid)
    if not uniform_rows:
        return np.array([]).reshape(0, 0)

    # 3. Filter selected rows by maximum length.
    max_length = 0
    for _, row in uniform_rows:
      max_length = max(max_length, _longest_uniform_subsequence(row))

    filtered_rows = []

    for i, row in uniform_rows:
      if _longest_uniform_subsequence(row) == max_length:
        filtered_rows.append((i,row))

    if not filtered_rows:
      return np.array([]).reshape(0,0)

    # 4. Order Selected Rows
    color_priority = [2, 8, 4, 1]  # Primary colors first
    other_colors = []
    color_to_rows = {}

    for i, row in filtered_rows:
      first_color = 0
      for val in row:
        if val != 0:
          first_color = val
          break
      if first_color not in color_to_rows:
          color_to_rows[first_color] = []
      color_to_rows[first_color].append((i,row))

    for color in color_to_rows:
      if color not in color_priority:
        other_colors.append(color)

    sorted_rows = []

    for color in color_priority + other_colors: #first priority colors
        if color in color_to_rows:
          for i, row in color_to_rows[color]:
            sorted_rows.append(row[:max_length])

    output_grid = np.array(sorted_rows)
    if output_grid.size == 0:
      return np.array([]).reshape(0, 0)

    return output_grid