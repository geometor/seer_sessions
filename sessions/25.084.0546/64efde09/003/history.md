
Previous Code:
```python
"""
1.  **Identify Top Row Pattern:** Observe the colors present on the first row (the top row pattern).
2.  **Random Row Replacement:** Randomly select rows in the input grid.
3.  **Insert Top Row Pattern:** Replace the selected rows with the colors from the top row, maintaining the column order.
4.    **Right-Side Color Expansion**: If, after insertion, colors other than the background color is on the last segment of the inserted row. The colors will be copied on top of the entire column below it.
5. **Preserve original rows**: If a row is not randomly selected for replacement, copy it to the output grid unchanged.
"""

import numpy as np
import random

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Top Row Pattern
    top_row_pattern = input_grid[0, :]

    # 2. & 3. Random Row Replacement and Insertion
    for y in range(height):
        # Decide if we replace (with a certain probability that needs tuning - using 50% for now)
        if random.random() < 0.5:  # 50% chance of replacement
            output_grid[y, :] = top_row_pattern

    # 4. Right-Side Color Expansion.
    for x in range(width):
        # Find last segment
        for y in range(height):
            if output_grid[y,x] != 8:
                last_non_azure = -1
                for k in range(width):
                    if output_grid[y,k]!=8:
                        last_non_azure = k
                if x == last_non_azure:
                    for row in range(y+1,height):
                       output_grid[row,x]= output_grid[y,x]
                #break; # uncomment later to see effect.
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 2 8 8 8 8 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 2 8 8 8 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 2 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 3 8 8 8 8 8 8 8 8 8
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 2 3 8 8 8 8 8 8 8 8 8
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 4 3 3 3 3 4 4 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 2 2 2 2 2 2 4 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 4 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 2 6 6 6 6 6
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 5 5 5 5 5
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 3 2 1 1 1 1 1
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 4 2 8 8 8 8 8
8 8 1 5 8 8 6 8 8 8 8 8 8 1 5 8 8 6 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 3 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 2 8 8 8 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 1 8 8 8 8 4 4 8 8 8 2 8 8 8 8 8
```
Match: False
Pixels Off: 218
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 57.82493368700267

## Example 2:
Input:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
3 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 4 2 2 2 2 2 2 4 4 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
9 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 9 8 6 8 3 8 8 8 8 8
3 3 3 3 3 1 4 8 8 8 8 8 8 8 8 8 8 9 8 6 8 3 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 8 8 8 8
6 6 6 6 6 1 2 8 8 8 8 8 8 8 4 2 2 2 2 2 2 4 4 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
9 9 9 9 9 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 3 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 6 6 6 6 6 6 6 6 6
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 9 9 9 9 9 9 9 9 9
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 4 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 8 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 4 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 2 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 4 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 1 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 1 8 6 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 109
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 38.447971781305114
Okay, let's analyze the results and refine the natural language program and the subsequent code.

**General Assessment:**

The initial approach of copying the top row and expanding colors on the rightmost edge has significant flaws. It doesn't capture the core logic of the transformations, especially evident in Example 2. The "right-side color expansion" is misinterpreting the actual rule, and the random row replacement is too simplistic. The core concept seems to involve identifying segments of non-background color (non-azure) in the *input* and propagating them downwards in specific columns, *but only if the entire row matches the pattern established in the top row, for segments of the row that are not azure (8)*. The random row replacement is not a valid part of the logic.

**Strategy for Resolving Errors:**

1.  **Discard Random Replacement:** The random row replacement is incorrect. We need to identify rows that *exactly* match the pattern of the first row (excluding azure pixels) and apply a transformation *only* to those rows.
2.  **Refine "Right-Side" Expansion:** It's not about the *rightmost* non-azure color. It's about propagating *any* non-azure color downwards *within its segment*, but only if its containing row has first been transformed to match the top row's non-azure pattern.
3. **Segment Identification**: The propagation happens within segments. A segment would be defined as consecutive pixels along x axis that has same color.

**Gather Metrics and Evidence:**

Let's use code execution to analyze Example 2 more closely, particularly the input and expected output, to pinpoint the exact transformation rule. We'll look for relationships between rows in the input and the output.



*code_execution:*
```python
import numpy as np

input_grid = np.array([
    [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 8, 8, 8, 8],
    [3, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 4, 2, 2, 2, 2, 2, 2, 4, 4, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [9, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])

expected_output = np.array([
    [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 8, 6, 8, 3, 8, 8, 8, 8, 8],
    [3, 3, 3, 3, 3, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 8, 6, 8, 3, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8],
    [6, 6, 6, 6, 6, 1, 2, 8, 8, 8, 8, 8, 8, 8, 4, 2, 2, 2, 2, 2, 2, 4, 4, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [9, 9, 9, 9, 9, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
])

top_row_input = input_grid[0]
top_row_output = expected_output[0]

print(f'{top_row_input=}')
print(f'{top_row_output=}')

for row_index in range(len(input_grid)):
    input_row = input_grid[row_index]
    output_row = expected_output[row_index]

    # Compare the non-azure segments
    input_non_azure = input_row[input_row != 8]
    output_non_azure = output_row[output_row != 8]

    if np.array_equal(input_non_azure,top_row_input[top_row_input!=8]):
        print(f"Row {row_index}: Input matches top row pattern (excluding azure).")



```

*code_execution_result:*
outcome: 1
```
top_row_input=array([8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 8, 8,
       8, 8, 8, 8, 8])
top_row_output=array([8, 8, 8, 8, 8, 1, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 8, 6, 8, 3,
       8, 8, 8, 8, 8])
Row 0: Input matches top row pattern (excluding azure).

```
**YAML Fact Extraction:**


```yaml
example_1:
  input:
    objects:
      - type: grid
        properties:
          rows: 26
          columns: 29
          background_color: azure (8)
          segments: [[4, 4], [2, 4], [2, 3]...] # Example segments
  output:
     objects:
      - type: grid
        properties:
          rows: 26
          columns: 29
          background_color: azure (8)
          segments: [[4,4], [2,4], [2,3]...]
  transformations:
      - action: copy_down
        condition: "row matches top row non-azure pattern"
        scope: "non-azure segments within the row"

example_2:
    input:
      objects:
        - type: grid
          properties:
            rows: 21
            columns: 27
            background_color: azure (8)
            segments: [[1, 4], [6], [1,4], [1,2]...] # Example segments

    output:
      objects:
       - type: grid
         properties:
            rows: 21
            columns: 27
            background_color: azure(8)

    transformations:
      - action: copy_down
        condition: "row matches top_row non-azure pattern"
        scope: "non-azure segments within the row"
```


**Natural Language Program:**

1.  **Identify the Top Row Pattern:** Examine the first row (the top row) of the input grid. Note the colors and their order, excluding any azure (8) pixels. This forms the "top row pattern".
2.  **Row Matching:** Iterate through each row of the input grid (excluding the top row itself).
3. **Conditional Row Transformation**: For each row:
    - Compare the colors of the current row (excluding azure pixels), with the "top row pattern" (also excluding azure).
    - If the non-azure colors of the current row exactly match the top row non-azure pattern, the row is eligible for transformation.

4.  **Segment-Based Propagation:** Within each *transformed* row:
    - Identify segments. A segment is defined as consecutive pixels of same value.
    - Iterate over the segments. For segments that are *not* azure:
       - For each non-azure pixel in the segment, copy its value downwards through all subsequent rows in the output grid, within the same column. If the pixel in same column below is transformed later, it overwrites the previous value.
5.  **Preserve Unmatched Rows**: If a row in the input grid does *not* match the top row pattern (excluding azure pixels), it is copied to the output grid *unchanged*.

