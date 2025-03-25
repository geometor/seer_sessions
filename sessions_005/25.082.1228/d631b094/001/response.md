```python
"""
1.  **Identify Non-Zero Values:** Examine the input grid and identify the non-zero color values, ignoring any cells with the value 0 (white).
2.  **Check repetition** Find which non-zero color is repeated.
3.  **Count Occurrences:** Count the number of times the identified non-zero repeated color appears in the input grid.
4.  **Construct Output Grid:** Create a new output grid. The output grid will be square. The side of the square is equal to the count from Step 3.
5.  **Populate Output:** Fill every cell of the output grid with the non-zero color identified in step 2.
"""

import numpy as np

def get_repeated_nonzero_color(grid):
    """
    Finds the repeated non-zero color in a grid.

    Args:
        grid: a numpy array
    Returns color or None
    """
    counts = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            val = grid[r,c]
            if val != 0:
                if val not in counts:
                    counts[val] = 0
                counts[val] += 1
    repeated_color = None
    for color, count in counts.items():
      if count > 1:
          if repeated_color is not None:
            return None #more than one repeated color
          repeated_color = color
    return repeated_color
def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)

    # Find the repeated non zero color
    repeated_color = get_repeated_nonzero_color(input_grid)

    if repeated_color is None:
       # Find the single non zero color if no repeats
       rows, cols = input_grid.shape
       for r in range(rows):
        for c in range(cols):
            val = input_grid[r,c]
            if val != 0:
              output_grid = np.full((1, 1), val)
              return output_grid.tolist()
    else:        
        # Count the occurrences of repeated non-zero color
        count = 0
        rows, cols = input_grid.shape
        for r in range(rows):
            for c in range(cols):
                if input_grid[r,c] == repeated_color:
                    count += 1

        # construct and populate output
        output_grid = np.full((count, count), repeated_color)

    return output_grid.tolist()
```