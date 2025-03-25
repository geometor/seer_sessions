
Previous Code:
```python
"""
The transformation rule focuses on expanding or shifting the azure (8) pixels in the top three rows based on their horizontal positions, while the bottom three rows (containing the yellow pixels) remain unchanged.
"""

import numpy as np

def get_azure_groups(row):
    """
    Finds groups of consecutive horizontally adjacent azure pixels in a row.
    Returns a list of tuples, each representing a group: (start_index, end_index).
    """
    groups = []
    in_group = False
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == 8:
            if not in_group:
                in_group = True
                start_index = i
        elif in_group:
            in_group = False
            groups.append((start_index, i - 1))
    if in_group:
        groups.append((start_index, len(row) - 1))
    return groups

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Process only the top three rows
    for row_index in range(3):
        row = input_grid[row_index]
        azure_groups = get_azure_groups(row)
        
        # Create a list to store the new positions of azure pixels
        new_azure_positions = []

        # collect column ranges that are occupied by azure
        ranges = []
        for group in azure_groups:
            ranges.append(list(range(group[0],group[1]+1)))
        
        # flatten ranges, convert to set, then back to list
        merged = sorted(list(set([item for sublist in ranges for item in sublist])))

        if len(merged) > 0:
          # occupy new positions with azure
          for col in merged:
            new_azure_positions.append(col)          
        
        # Clear existing azure pixels in the output row
        for i, pixel in enumerate(output_grid[row_index]):
            if pixel == 8:
                output_grid[row_index, i] = 0

        # Set azure pixels at the new positions
        for pos in new_azure_positions:
            output_grid[row_index, pos] = 8

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Expected Output:
```
8 0 8 8 0 8 0 0 0
8 8 0 0 8 8 0 0 0
8 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Transformed Output:
```
0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
![Transformed Image](760b3cac-1.png)
match: False
pixels_off: 5
size_correct: True
color_palette_correct: True
correct_pixel_counts: None

## Example 2:
Input:
```
0 0 0 8 0 8 0 0 0
0 0 0 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Expected Output:
```
0 0 0 8 0 8 8 0 8
0 0 0 8 8 8 8 8 8
0 0 0 8 8 0 0 8 8
0 0 0 0 0 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Transformed Output:
```
0 0 0 8 0 8 0 0 0
0 0 0 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
![Transformed Image](760b3cac-2.png)
match: False
pixels_off: 7
size_correct: True
color_palette_correct: True
correct_pixel_counts: None

## Example 3:
Input:
```
0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Expected Output:
```
0 0 8 8 0 0 0 0 0
8 8 0 0 8 8 0 0 0
0 0 8 8 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
Transformed Output:
```
0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```
![Transformed Image](760b3cac-3.png)
match: False
pixels_off: 4
size_correct: True
color_palette_correct: True
correct_pixel_counts: None
