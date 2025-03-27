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