# 7837ac64 • 012 • refine_coder

---
```python
"""
Finds all occurrences of a 2x2 pattern in the input grid where the top-left cell is blue (1) and the bottom-left cell is green (3).
Replaces each occurrence with a 2x1 pattern in the output grid: blue (1) on top and green (3) on the bottom.
The output grid has same dimensions as input, and unmatched areas are filled with white/background (0).
"""

import numpy as np

def find_pattern_occurrences(input_grid, input_pattern):
    """
    Finds all occurrences of the input_pattern within the input_grid.

    Args:
        input_grid: The input grid (2D numpy array).
        input_pattern: The 2x2 pattern to search for (2D numpy array).

    Returns:
        A list of (y, x) coordinates of the top-left corner of each match.
    """
    occurrences = []
    input_height, input_width = input_grid.shape
    pattern_height, pattern_width = input_pattern.shape

    for y in range(input_height - pattern_height + 1):
        for x in range(input_width - pattern_width + 1):
            match = True
            for py in range(pattern_height):
                for px in range(pattern_width):
                    # Check for the specific pattern: [[1, any], [3, any]]
                    if py == 0 and px == 0:
                        if input_grid[y + py, x + px] != input_pattern[py, px]:
                            match = False
                            break
                    elif py == 1 and px == 0:
                         if input_grid[y+py, x+px] != input_pattern[py,px]:
                            match = False
                            break
                if not match:
                    break
            if match:
                occurrences.append((y, x))
    return occurrences

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)
    input_height, input_width = input_array.shape

    # Initialize the output grid as all zeros (white) with same dims as input
    output_grid = np.zeros((input_height, input_width), dtype=int)

    # Define the input pattern: [[1, _], [3, _]]  (_ means any value)
    input_pattern = np.array([[1], [3]])

    # Find all occurrences of the input pattern
    occurrences = find_pattern_occurrences(input_array, input_pattern)

    # Create the output pattern: [[1], [3]]
    output_pattern = np.array([[1], [3]])
    output_height, output_width = output_pattern.shape

    # Place the output pattern in the output grid for each occurrence
    for y, x in occurrences:
        for py in range(output_height):
            for px in range(output_width):
                output_grid[y + py, x + px] = output_pattern[py, px]

    return output_grid.tolist()
```
