"""
1.  **Count 2x2 Blocks**: Examine the input grid and count the number of 2x2 blocks of uniform color. Keep separate counts for each color.
2.  **All Same Color (Not Blue)**: If all pixels in the input grid are the same color, *and* that color is not blue (1), the output is a 1x1 grid containing only the value 0.
3.  **Mixed Colors**: Create an output grid with width equal to the total 2x2 block count (sum of 2x2 blocks of *any* uniform color).
      For each blue block, add '1' to output.
      For each non-blue block, add a '0' to the output.
4. Return the resulting array.
"""

import numpy as np

def count_2x2_blocks(input_grid):
    """Counts the number of 2x2 blocks of the same color, for all colors."""
    counts = {}
    rows, cols = input_grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            block = input_grid[i:i+2, j:j+2]
            if np.all(block == block[0, 0]):
                color = block[0, 0]
                counts[color] = counts.get(color, 0) + 1
    return counts

def transform(input_grid):
    # Count the 2x2 blocks for all colors.
    block_counts = count_2x2_blocks(np.array(input_grid))

    input_grid = np.array(input_grid)

    # All same non-blue color
    if np.all(input_grid == input_grid[0,0]) and input_grid[0,0] != 1:
      return np.array([[0]])

    # Calculate total 2x2 blocks
    total_blocks = sum(block_counts.values())
    
    # if we have any blocks, return a 1xN grid
    if total_blocks > 0:
      output_grid = []
      for color, count in block_counts.items():
          if color == 1: # blue
            for _ in range(count):
              output_grid.append(1)
          else:
            for _ in range(count):
              output_grid.append(0)
      return np.array([output_grid])

    return np.array([[0]])