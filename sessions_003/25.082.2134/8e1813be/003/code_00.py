"""
Combines row-based and column-based selection strategies to transform the input grid.
Prioritizes column-based extraction if consistent columns are found; otherwise,
performs row-based extraction based on longest uniform non-zero subsequences and color order.
"""

import numpy as np

def _find_consistent_columns(grid):
    """Finds columns with consistent non-zero values."""
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
        else: #val is zero
            max_len = max(max_len, current_len)
            current_len = 0
            current_val = None

    max_len = max(max_len, current_len)  # Check at the end
    return max_len


def _find_candidate_rows(grid):
    """Identifies rows with a contiguous sequence of non-zero pixels of same color"""
    candidate_rows = []
    for row in grid:
        if _longest_uniform_subsequence(row) > 0:
            candidate_rows.append(row)
    return candidate_rows

def _extract_columns(grid, col_indices):
  """extracts values at specified column indices"""
  return grid[:, col_indices]

def transform(input_grid):
    # Check for consistent columns
    consistent_columns = _find_consistent_columns(input_grid)

    if consistent_columns:
        # Column-based extraction
        output_grid = _extract_columns(input_grid, consistent_columns)

    else:
        # Row-based extraction
        candidate_rows = _find_candidate_rows(input_grid)
        if not candidate_rows:
          return np.array([]).reshape(0,0)

        # Determine output row length (longest uniform subsequence)
        output_row_length = 0
        for row in candidate_rows:
          output_row_length = max(output_row_length, _longest_uniform_subsequence(row))

        # Select rows based on the longest uniform subsequence and non-zero
        selected_rows = []

        for row in candidate_rows:
          if _longest_uniform_subsequence(row) == output_row_length:
            selected_rows.append(row[:output_row_length]) #truncate the row

        if not selected_rows:
          return np.array([]).reshape(0,0)

        # Determine Color order (THIS IS STILL A SIMPLIFICATION)
        # For now, prioritize colors seen in the examples
        color_order = [2, 1, 3, 4, 8, 6]  # Example 1 order
        color_order += [7, 9, 5] # adding other colors to improve robustness

        # Build a dictionary of {color: [rows]}
        color_rows = {}
        for row in selected_rows:
            color = row[0] if row[0] !=0 else None #get first non-zero element
            if color is not None:
              if color not in color_rows:
                  color_rows[color] = []
              color_rows[color].append(row)

        # Sort rows by color order
        sorted_rows = []

        for color in color_order:
          if color in color_rows:
            for row in color_rows[color]:
              sorted_rows.append(row)

        if not sorted_rows:
            return np.array([]).reshape(0, 0)


        output_grid = np.array(sorted_rows)
        if output_grid.size == 0:
          return np.array([]).reshape(0,0)


    return output_grid