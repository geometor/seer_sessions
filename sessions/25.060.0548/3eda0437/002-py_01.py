"""
Iterate through the input grid. Identify contiguous sequences of white (0) pixels.
For each white (0) sequence, check if it is directly adjacent to azure (1) pixels on any side.
If a white (0) sequence is adjacent to azure (1) pixels, replace those white (0) pixels with magenta (6) pixels.
The output grid is the result of these replacements.
"""

import numpy as np

def get_contiguous_sequences(row):
    """
    Finds contiguous sequences of the same value in a row.
    Returns a list of (start_index, end_index, value) tuples.
    """
    sequences = []
    if not row.size:
        return sequences

    start = 0
    current_value = row[0]
    for i in range(1, len(row)):
        if row[i] != current_value:
            sequences.append((start, i - 1, current_value))
            start = i
            current_value = row[i]
    sequences.append((start, len(row) - 1, current_value))
    return sequences

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
      row_sequences = get_contiguous_sequences(input_grid[i,:])
      
      #check each row
      for start, end, value in row_sequences:
        if value == 0: #if white
          if end+1 < cols and input_grid[i,end+1] == 1: #if blue to the right
            for j in range(start,end+1):
              output_grid[i,j] = 6
    
    # Iterate through each column
    for j in range(cols):
      col_sequences = get_contiguous_sequences(input_grid[:,j])
          
      #check each column
      for start, end, value in col_sequences:
        if value == 0: #if white
          if end+1 < rows and input_grid[end+1,j] == 1: #if blue to the bottom
            for i in range(start,end+1):
              output_grid[i,j] = 6

    return output_grid