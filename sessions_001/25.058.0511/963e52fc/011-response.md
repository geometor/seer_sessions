# 963e52fc • 011 • refine_coder

---
```python
"""
1.  **Identify the Pattern Row:** Find the single row in the input grid that contains non-zero (non-white) pixels.
2.  **Extract the Pattern:** Extract the sequence of non-zero pixel values from that row. This sequence consists of alternating 2s (red) and 3s (green).
3. Determine input pattern length: Count how many non-zero pixels are in the input pattern row.
4. Determine how much the pattern repeats in input.
5. Determine how much the pattern repeats in output.
6.  **Extend the Pattern:** Create a new row. Repeat the extracted pattern. The length of the repeating pattern follows: output_width = input_width + pattern length * (output repetitions - input repetitions)
7. **Preserve Row:** Create a output where all other rows are filled with zeros and the output pattern is placed at the same index in the output grid.
"""

import numpy as np

def get_pattern_row_index(grid):
    # Find the index of the row with non-zero elements
    non_zero_rows = np.where(np.any(grid != 0, axis=1))[0]
    if len(non_zero_rows) > 0:
      return non_zero_rows[0]
    return -1

def get_pattern(grid):
  # extract the non-zero pattern
  row_index = get_pattern_row_index(grid)
  if row_index == -1:
    return []
  row = grid[row_index]
  return row[row != 0]

def calculate_output_width(input_grid, output_grid):
    # calculate width
    input_pattern = get_pattern(input_grid)
    input_pattern_len = len(input_pattern)
    input_repetitions = input_pattern_len // 2

    output_pattern = get_pattern(output_grid)
    output_repetitions = len(output_pattern) // 2
    
    input_width = input_grid.shape[1]

    output_width = input_width + 2 * (output_repetitions - input_repetitions)
    return output_width

def transform(input_grid):
    # make input grid numpy array
    input_grid = np.array(input_grid)

    # Find pattern and index
    pattern_row_index = get_pattern_row_index(input_grid)
    pattern = get_pattern(input_grid)

    # dummy output grid for calculating output width
    dummy_output = [([0] * (len(pattern)*2))]
    output_width = calculate_output_width(input_grid, np.array(dummy_output))
    
    # Initialize the output grid with zeros, same height as input, calculated width
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)

    # if valid pattern
    if(len(pattern) > 0):
      # Calculate repetitions needed
      output_pattern_len = output_width - (input_grid.shape[1] - len(pattern))
      
      # build the output row
      output_row = np.tile(pattern[:2], output_pattern_len // 2)

      # Insert the extended pattern into the correct row
      output_grid[pattern_row_index, :len(output_row)] = output_row

    return output_grid
```
