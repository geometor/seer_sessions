```python
import math
from typing import List, Dict, Tuple

"""
Transforms an input grid by identifying the column with the maximum number of non-zero elements.
If multiple columns share the maximum count, the rightmost column (highest index) is chosen.
The output grid is initialized with zeros and then populated only with the values from the selected column of the input grid.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D integer grid.

    Returns:
        A list of lists representing the transformed 2D integer grid.
    """

    # Handle empty input grid
    if not input_grid:
        return []
    
    rows = len(input_grid)
    if rows == 0:
        return []
        
    cols = len(input_grid[0])
    if cols == 0:
        # Return a grid of empty rows with the same number of rows as input
        return [[] for _ in range(rows)] 

    # Initialize output_grid with zeros, matching input dimensions
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # --- Step 1 & 2: Calculate non-zero counts for each column ---
    non_zero_counts: Dict[int, int] = {}
    for j in range(cols):
        count = 0
        for i in range(rows):
            if input_grid[i][j] != 0:
                count += 1
        non_zero_counts[j] = count

    # --- Step 3: Determine the maximum non-zero count ---
    if not non_zero_counts: # Should only happen if cols is 0, handled above
         return output_grid 
         
    max_count = -1 # Initialize to handle cases where all elements might be zero
    # Find the maximum value among the counts
    # Using max() on values is efficient, default handles empty list case correctly if needed
    # but we check non_zero_counts dict explicitly above.
    # Add a check for the case where the dictionary might be empty, though unlikely here.
    if non_zero_counts:
      max_count = max(non_zero_counts.values())
    else:
       # If somehow the dictionary is empty despite cols > 0, return the zero grid
       return output_grid


    # --- Step 4 & 5: Identify the target column index (rightmost tie-breaker) ---
    target_col_index = -1
    # Iterate from right to left to find the first column (rightmost) with the max count
    for j in range(cols - 1, -1, -1):
        if non_zero_counts[j] == max_count:
            target_col_index = j
            break # Found the rightmost column with max count

    # --- Step 6: Copy the selected column to the output grid ---
    # Check if a valid target column was found (handles all-zero grid where max_count is 0)
    if target_col_index != -1:
        for i in range(rows):
            output_grid[i][target_col_index] = input_grid[i][target_col_index]

    # --- Step 7: Return the final output grid ---
    return output_grid

```