# f9012d9b • 012 • refine_coder

---
```python
"""
1.  Identify Unique Values: Determine all the unique pixel values present in the input grid.
2.  Count Occurrences: For each unique value, count how many times it appears in the grid.
3.  Find Dominant Values: Select the value(s) with the highest number of occurrences. A value will be considered *dominant* if it is the most frequently appearing value.
4.  Select Highest Value: If there are multiple most frequent values, select the largest numerical value among them.
5.  Output: Create a 1x1 grid containing the selected value.
"""

import numpy as np

def get_dominant_value(grid):
    # Count the occurrences of each unique value in the grid.
    unique_values, counts = np.unique(grid, return_counts=True)
    
    # Find the maximum count.
    max_count = np.max(counts)
    
    # Get all values that have the maximum count.
    dominant_values = unique_values[counts == max_count]
    
    # Return the highest of the dominant values.
    return np.max(dominant_values)

def transform(input_grid):
    """
    Transforms an input grid into a 1x1 grid containing the most frequent value,
    or the largest of the most frequent values if there's a tie.
    """
    # Find the dominant (most frequent) value in the input grid.
    dominant_value = get_dominant_value(input_grid)

    # Create a 1x1 grid with the dominant value.
    output_grid = np.array([[dominant_value]])

    return output_grid
```
