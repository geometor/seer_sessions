"""
1. **Extract:** Identify and extract all non-zero pixels (colored pixels) from the input grid, noting their original values.
2. **Reorder:** Reorder the non zero numbers into a new sequence. The sequence will be bottom-left element in input is first, then moving up that column, wrapping to next column to the right when the top is reached.
3. **Arrange:** Populate the 3x3 output grid with the reordered non-zero pixels.
"""

import numpy as np

def transform(input_grid):
    # Extract non-zero pixels and their coordinates
    non_zero_pixels = []
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
          if input_grid[r, c] != 0:
              non_zero_pixels.append((input_grid[r,c], r, c))

    # Reorder based on column-wise traversal from bottom-left
    reordered_pixels = sorted(non_zero_pixels, key=lambda x: (x[2], -x[1]))
    reordered_values = [pixel[0] for pixel in reordered_pixels]


    # Arrange into a 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    #fill output, add padding with zeros if needed
    for i in range(min(len(reordered_values),9)):
      row = i // 3
      col = i % 3
      output_grid[row, col] = reordered_values[i]


    return output_grid